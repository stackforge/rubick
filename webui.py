from StringIO import StringIO

from bson.objectid import ObjectId
import os.path
from flask import Flask, request, json, send_file
from flask_wtf import Form
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException
from pymongo import MongoClient
from recordtype import recordtype
from rubick.celery import app as celery, \
    ostack_inspect_task, InspectionRequest
from rubick.common import Inspection, Issue
from rubick.discovery import OpenstackDiscovery
from rubick.json import openstack_for_json
from rubick.model import Openstack
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired
import wtforms_json

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3fooN]LWX/,?RT'

wtforms_json.init()


def connect_to_db():
    mongo_url = os.environ.get("MONGODB_URI") or "mongodb://localhost/rubick"
    client = MongoClient(mongo_url)
    return client[mongo_url.split('/')[-1]]


def get_db():
    db = connect_to_db()
    return db


def is_key_valid(private_key):
    for key_klass in [RSAKey, DSSKey]:
        try:
            key_klass.from_private_key(StringIO(private_key))
            return True
        except SSHException:
            pass

    return False


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
    if 'nodes' in data and (isinstance(data['nodes'], str) or
                            isinstance(data['nodes'], unicode)):
        data['nodes'] = data['nodes'].split()

    if not 'name' in data or data['name'] == '':
        errors['name'] = ['Cluster name is required']
    if not 'nodes' in data or data['nodes'] == []:
        errors['nodes'] = ['At least one cluster node is required']
    if not 'private_key' in data:
        errors['private_key'] = ['Private key for accessing nodes is required']
    elif not is_key_valid(data['private_key']):
        errors['private_key'] = ['Private key format is unknown']

    if len(errors) == 0:
        cluster = Cluster(**data)

        get_db()['clusters'].save(cluster.as_doc())
        return '', 201
    else:
        return json.dumps(dict(errors=errors)), 422


@app.route('/clusters/<id>', methods=['DELETE'])
def del_cluster(id):
    get_db()['clusters'].remove({'_id': ObjectId(id)})
    return '', 200


@app.route('/clusters/test', methods=['POST'])
def test_cluster():
    data = json.loads(request.data)
    errors = {}
    if not 'nodes' in data or data['nodes'] == []:
        errors['nodes'] = ['At least one cluster node is required']
    if not 'private_key' in data:
        errors['private_key'] = ['Private key for accessing nodes is required']
    elif not is_key_valid(data['private_key']):
        errors['private_key'] = ['Private key format is unknown']

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
        cluster_doc = db['clusters'].find_one({
            '_id': ObjectId(form.cluster_id.data)})
        if not cluster_doc:
            return json.dumps({'errors': {
                'cluster_id': 'Cluster not found'}}), 404

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
        result = job.result.value

        if isinstance(result, Openstack):
            return json.dumps({
                'state': 'success',
                'result': openstack_for_json(result)})
        else:
            return json.dumps({'state': 'failure', 'message': result})
    else:
        return json.dumps({'state': str(job.state).lower()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
