from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
app.config['SECRET_KEY'] = '45cf93c4d41348cd9980674ade9a7356'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)
metrics.info('task_manager_app_info', 'Task Manager Flask application', version='1.0.0')

login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# Always put Routes at end
from todo_project import routes
