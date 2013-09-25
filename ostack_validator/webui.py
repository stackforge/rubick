from flask import Flask, request, redirect, render_template, json
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from ostack_validator.celery import app as celery, ostack_inspect_task

app = Flask(__name__)
Bootstrap(app)
app.debug = True
app.config.update(
  WTF_CSRF_SECRET_KEY = 'foo bar baz'
)
app.secret_key = 'A0Zr98j/3fooN]LWX/,?RT'


class ValidationLaunchForm(Form):
  nodes = StringField('Nodes', validators=[DataRequired()])
  username = StringField('Username', default='root', validators=[DataRequired()])
  private_key = TextAreaField('Private Key', validators=[DataRequired()])

  launch = SubmitField('Launch validation')

@app.route('/')
def index():
  return redirect('/validation')

@app.route('/validation', methods=['GET', 'POST'])
def launch_validation():
  form = ValidationLaunchForm()
  if form.validate_on_submit():
    nodes = form.nodes.data.split(' ')
    username = form.username.data
    private_key = form.private_key.data

    job = ostack_inspect_task.delay(nodes=nodes, username=username, private_key=private_key)

    return redirect('/validation/%s' % job.id)
  else:
    return render_template('validation_form.html', form=form)

@app.route('/validation/<id>')
def job(id):
  job = celery.AsyncResult(id)
  if job.ready():
    return 'Result is %s' % job.result
  else:
    return 'State is %s' % job.state

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

