from itertools import groupby
import os.path

from flask import Flask, request, redirect, render_template, json, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
import wtforms_json
from pymongo import MongoClient
from recordtype import recordtype

from ostack_validator.celery import app as celery, ostack_inspect_task, InspectionRequest
from ostack_validator.common import Inspection, Issue, MarkedIssue
from ostack_validator.model import Openstack

app = Flask(__name__,
            static_folder='config-validator-ui-concept',
            static_url_path='/static')
Bootstrap(app)
app.secret_key = 'A0Zr98j/3fooN]LWX/,?RT'

wtforms_json.init()

def connect_to_db():
    mongo_url = os.environ.get("MONGODB_URI") or "mongodb://localhost/rubick"
    client = MongoClient(mongo_url)
    return client[mongo_url.split('/')[-1]]

def get_db():
    db = connect_to_db()
    return db

class Cluster(object):
  @classmethod
  def from_doc(klass, doc):
    return Cluster(doc['id'], doc['name'], description=doc['description'], status=doc['status'], seed_nodes=doc['seed_nodes'], nodes=doc['nodes'], private_key=doc['private_key'])

  def __init__(self, id, name, description=None, status='Unknown', seed_nodes=[], private_key=None, nodes=[]):
    super(Cluster, self).__init__()
    self.id = id
    self.name = name
    self.description = description
    self.status = status
    self.seed_nodes = seed_nodes
    self.private_key = private_key
    self.nodes = nodes

  # JSON serialization helper
  def _asdict(self):
    return dict(id=self.id, name=self.name, description=self.description, status=self.status, nodes=self.nodes, seed_nodes=self.seed_nodes, private_key=self.private_key)

class RuleGroup:
  VALIDITY='validity'
  HA='high-availability'
  BEST_PRACTICES='best-practices'

  all = [VALIDITY, HA, BEST_PRACTICES]

class Rule(object):
  @classmethod
  def from_doc(klass, doc):
    return Rule(doc['id'], doc['group'], doc['name'], doc['text'])

  def __init__(self, id, group, name, text):
    super(Rule, self).__init__()
    self.id = id
    self.group = group
    self.name = name
    self.text = text

  # JSON serialization helper
  def _asdict(self):
    return dict(id=self.id, group=self.group, name=self.name, text=self.text)

class ClusterForm(Form):
  name = StringField('Name', validators=[DataRequired()])
  nodes = StringField('Nodes', validators=[DataRequired()])
  private_key = TextAreaField('Private Key', validators=[DataRequired()])

class ValidateClusterForm(Form):
  cluster_id = StringField('Cluster', validators=[DataRequired()])
  rules = SelectMultipleField('Rules')

wtforms_json.init()


def connect_to_db():
    mongo_url = os.environ.get("MONGODB_URI") or "mongodb://localhost/rubick"
    client = MongoClient(mongo_url)
    return client[mongo_url.split('/')[-1]]


def get_db():
    db = connect_to_db()
    return db


Cluster = recordtype('Cluster',
                     ['_id', 'name', 'description', 'status', 'nodes'],
                     default=None)


class RuleGroup:
    VALIDITY = 'validity'
    HA = 'high-availability'
    BEST_PRACTICES = 'best-practices'

    all = [VALIDITY, HA, BEST_PRACTICES]


class ClusterForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    seed_nodes = StringField('Initial nodes', validators=[DataRequired()])
    private_key = TextAreaField('Private Key', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, csrf_enabled=False, **kwargs)


class ValidateClusterForm(Form):
    cluster_id = StringField('Cluster', validators=[DataRequired()])
    rules = SelectMultipleField('Rules')

    def __init__(self):
        super(ClusterForm, self).__init__(csrf_enabled=False)


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
    #db = get_db()
    #return json.dumps([Cluster.from_doc(doc) for doc in db['clusters'].find()])
    return json.dumps([
        Cluster(
            id='cluster1',
            name="Kirill's DevStack",
            description="Grizzly-based devstack with Quantum and oVS, deployed on Kirill's laptop",
            status='Available'),
        # Cluster(
        #     id='cluster2',
        #     name="Peter's DevStack",
        #     description="Grizzly-based devstack deployed on Peter Lomakin's workstation with nova-network and FlatDHCP manager",
        #     status='Broken')
    ])


@app.route('/clusters', methods=['POST'])
def add_cluster():
    form = ClusterForm.from_json(json.loads(request.data))
    if form.validate():
        cluster = Cluster()
        form.populate_obj(cluster)
        get_db()['clusters'].save(cluster.asdict())
        return '', 201
    else:
        return json.dumps(dict(errors=form.errors)), 422


@app.route('/rules')
def get_rules():
    rules = []
    for inspection in Inspection.all_inspections():
        rules.extend(inspection.rules())

#     rules = [Rule.from_doc(doc) for doc in db['rules'].find()]
#     rules = [
#         Rule(id='rule1', group=RuleGroup.VALIDITY,
#              name='Nova has proper Keystone host',
#              description="""Given I use OpenStack Grizzly 2013.1
# And Nova has "auth_strategy" equal to "keystone"
# And Keystone addresses are @X
# Then Nova should have "keystone_authtoken.auth_host" in "$X" """),
#         Rule(id='rule1', group=RuleGroup.VALIDITY,
#              name='Nova has proper Keystone host',
#              description="""Given I use OpenStack Grizzly 2013.1
# And Nova has "auth_strategy" equal to "keystone"
# And Keystone addresses are @X
# Then Nova should have "keystone_authtoken.auth_host" in "$X" """)]
    return json.dumps(rules)


@app.route('/rules/<group>')
def get_rules_group(group):
    if not group in RuleGroup.all:
        return 'Unknown rule group "%s"' % group, 404

    #db = get_db()
    #rules = [Rule.from_doc(doc) for doc in db['rules'].find({'group': group})]
    #return json.dumps(rules)
    return get_rules()


@app.route('/validation', methods=['GET', 'POST'])
def launch_validation():
    form = ValidationLaunchForm()
    if form.validate_on_submit():
        request = InspectionRequest(
            form.nodes.data.split(
                ' '),
            form.username.data,
            private_key=form.private_key.data)

        job = ostack_inspect_task.delay(request)

        return redirect('/validation/%s' % job.id)
    else:
        return render_template('validation_form.html', form=form)


@app.route('/validation/<id>')
def job(id):
    job = celery.AsyncResult(id)
    if job.ready():
        r = job.result.request

        form = ValidationLaunchForm()
        form.nodes.data = ' '.join(r.nodes)
        form.username.data = r.username
        form.private_key.data = r.private_key

        openstack = job.result.value

        if isinstance(openstack, Openstack):
            issue_source_f = lambda i: i.mark.source if isinstance(
                i, MarkedIssue) else None
            source_groupped_issues = groupby(
                sorted(openstack.issues,
                       key=issue_source_f),
                key=issue_source_f)

            return (
                render_template(
                    'validation_result.html',
                    form=form,
                    openstack=openstack,
                    grouped_issues=source_groupped_issues)
            )
        else:
            return (
                render_template(
                    'validation_error.html',
                    form=form,
                    message=openstack)
            )
    else:
        return render_template('validation_state.html', state=job.state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
