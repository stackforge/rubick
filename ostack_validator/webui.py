from itertools import groupby

from flask import Flask, request, redirect, render_template, json
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from ostack_validator.celery import app as celery, ostack_inspect_task, InspectionRequest
from ostack_validator.common import Issue, MarkedIssue
from ostack_validator.model import Openstack

app = Flask(__name__)
Bootstrap(app)
app.debug = True
app.config.update(
    WTF_CSRF_SECRET_KEY='foo bar baz'
)
app.secret_key = 'A0Zr98j/3fooN]LWX/,?RT'


class ValidationLaunchForm(Form):
    nodes = StringField('Nodes', validators=[DataRequired()])
    username = StringField(
        'Username',
        default='root',
        validators=[DataRequired()])
    private_key = TextAreaField('Private Key', validators=[DataRequired()])

    launch = SubmitField('Launch validation')


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
    return redirect('/validation')


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
    app.run(host='0.0.0.0', debug=True)
