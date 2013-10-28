from StringIO import StringIO

from bson.objectid import ObjectId
import os.path
from flask import Flask, request, json, send_file
from flask_wtf import Form
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired
import wtforms_json


from rubick.celery import app as celery, \
    ostack_discover_task, ostack_inspect_task, InspectionRequest
from rubick.common import Inspection, Issue
from rubick.database import get_db, Cluster, RuleGroup
from rubick.discovery import OpenstackDiscovery
from rubick.json import openstack_for_json
from rubick.model import Openstack


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3fooN]LWX/,?RT'

wtforms_json.init()


def is_key_valid(private_key):
    for key_klass in [RSAKey, DSSKey]:
        try:
            key_klass.from_private_key(StringIO(private_key))
            return True
        except SSHException:
            pass

    return False


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

    if len(errors) > 0:
        return json.dumps(dict(errors=errors)), 422

    cluster = Cluster(**data)

    cluster_id = get_db()['clusters'].save(cluster.as_doc())

    ostack_discover_task.delay(str(cluster_id))

    return json.dumps(dict(id=str(cluster_id))), 201


@app.route('/clusters/<cluster_id>', methods=['GET'])
def get_cluster(cluster_id):
    cluster_doc = get_db()['clusters'].find_one({'_id': ObjectId(cluster_id)})
    if not cluster_doc:
        return json.dumps({'errors': {'cluster_id': 'Cluster not found'}}), 404

    cluster = Cluster.from_doc(cluster_doc)

    return json.dumps(cluster.for_json()), 200


@app.route('/clusters/<cluster_id>', methods=['DELETE'])
def del_cluster(cluster_id):
    get_db()['clusters'].remove({'_id': ObjectId(cluster_id)})
    return '', 200


@app.route('/clusters/<cluster_id>/rediscover', methods=['GET'])
def discover_cluster(cluster_id):
    cluster_doc = get_db()['clusters'].find_one({'_id': ObjectId(cluster_id)})
    if not cluster_doc:
        return json.dumps({'errors': {'cluster_id': 'Cluster not found'}}), 404

    ostack_discover_task.delay(cluster_id)

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
