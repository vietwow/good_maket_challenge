from flask import Flask, g
from resp import *
from model import database

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.errorhandler(400)
def handle_400(err):
    return error('Invalid JSON body')

@app.before_request
def before_request():
    # Do connect database
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response


# Here for register BluePrint routes

from views import users, teams, projects, tasks

app.register_blueprint(users.module, url_prefix="/api/v1/users")
app.register_blueprint(teams.module, url_prefix="/api/v1/teams")
app.register_blueprint(projects.module, url_prefix="/api/v1/projects")
app.register_blueprint(tasks.module, url_prefix="/api/v1/tasks")


if __name__ == "__main__":
    app.debug=True
    app.run()
