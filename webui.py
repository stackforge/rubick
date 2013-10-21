import os.path

from flask import Flask, request, json, send_file
from flask_wtf import Form
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired
import wtforms_json
from pymongo import MongoClient
from recordtype import recordtype

from ostack_validator.celery import app as celery, ostack_inspect_task, InspectionRequest
from ostack_validator.common import Inspection, Issue
from ostack_validator.model import Openstack
from ostack_validator.discovery import OpenstackDiscovery

app = Flask(__name__,
            static_folder='config-validator-ui-concept',
            static_url_path='/static')
app.secret_key = 'A0Zr98j/3fooN]LWX/,?RT'

wtforms_json.init()


def connect_to_db():
    mongo_url = os.environ.get("MONGODB_URI") or "mongodb://localhost/rubick"
    client = MongoClient(mongo_url)
    return client[mongo_url.split('/')[-1]]


def get_db():
    db = connect_to_db()
    return db


class Cluster(recordtype('Cluster',
                         ['id', 'name', 'description',
                          'status', 'nodes', 'private_key'],
                         default=None)):
    @classmethod
    def from_doc(klass, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return Cluster(**doc)

    def as_doc(self):
        return self._asdict()


class RuleGroup:
    VALIDITY = 'validity'
    HA = 'high-availability'
    BEST_PRACTICES = 'best-practices'

    all = [VALIDITY, HA, BEST_PRACTICES]


class ValidateClusterForm(Form):
    cluster_id = StringField('Cluster', validators=[DataRequired()])
    rules = SelectMultipleField('Rules')

    def __init__(self):
        super(ValidateClusterForm, self).__init__(csrf_enabled=False)


@app.template_filter()
def to_label(s):
    if s in [Issue.FATAL, Issue.ERROR]:
        return 'label-danger'
    elif s == Issue.WARNING:
        return 'label-warning'
    else:
        return 'label-info'


@app.route('/')
def index():
    return send_file(os.path.join(app.static_folder, 'index.html'))


@app.route('/clusters')
def get_clusters():
    db = get_db()
    return json.dumps([Cluster.from_doc(doc) for doc in db['clusters'].find()])


@app.route('/clusters', methods=['POST'])
def add_cluster():
    data = json.loads(request.data)
    errors = {}
    if not 'name' in data or data['name'] == '':
        errors['name'] = ['Cluster name is required']
    if not 'nodes' in data or data['nodes'] == []:
        errors['nodes'] = ['At least one cluster node is required']
    if not 'private_key' in data:
        errors['private_key'] = ['Private key for accessing nodes is required']

    if len(errors) == 0:
        cluster = Cluster(**data)

        get_db()['clusters'].save(cluster.as_doc())
        return '', 201
    else:
        return json.dumps(dict(errors=errors)), 422


@app.route('/clusters/<id>', methods=['DELETE'])
def del_cluster(id):
    get_db()['clusters'].remove({'_id': id})
    return '', 200


@app.route('/clusters/test', methods=['POST'])
def test_cluster():
    data = json.loads(request.data)
    errors = {}
    if not 'nodes' in data or data['nodes'] == []:
        errors['nodes'] = ['At least one cluster node is required']
    if not 'private_key' in data:
        errors['private_key'] = ['Private key for accessing nodes is required']

    if len(errors) == 0:
        d = OpenstackDiscovery()
        if d.test_connection(data['nodes'], private_key=data['private_key']):
            return '', 200
        else:
            return '', 409
    else:
        return json.dumps(dict(errors=errors)), 422


@app.route('/rules')
def get_rules():
    rules = []
    for inspection in Inspection.all_inspections():
        rules.extend(inspection.rules())

    return json.dumps(rules)


@app.route('/rules/<group>')
def get_rules_group(group):
    if not group in RuleGroup.all:
        return 'Unknown rule group "%s"' % group, 404

    #db = get_db()
    #rules = [Rule.from_doc(doc) for doc in db['rules'].find({'group': group})]
    #return json.dumps(rules)
    return get_rules()


@app.route('/validation', methods=['POST'])
def launch_validation():
    form = ValidateClusterForm()
    if form.validate_on_submit():
        db = get_db()
        cluster_doc = db['clusters'].find_one({'_id': form.cluster_id.data})
        if not cluster_doc:
            return json.dumps({'errors': {'cluster_id': 'Not found'}}), 404

        cluster = Cluster.from_doc(cluster_doc)
        request = InspectionRequest(
            cluster.nodes,
            username='root',
            private_key=cluster.private_key)

        job = ostack_inspect_task.delay(request)

        return json.dumps({'id': job.id}), 202
    else:
        return json.dumps(dict(errors=form.errors)), 422


@app.route('/validation/<id>')
def job(id):
    job = celery.AsyncResult(id)
    if job.ready():
        openstack = job.result.value

        if isinstance(openstack, Openstack):
            return json.dumps(openstack)
        else:
            return json.dumps({'error': openstack})
    else:
        return json.dumps({'state': job.state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
