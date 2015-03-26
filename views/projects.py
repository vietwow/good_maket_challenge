from flask import Blueprint, abort, jsonify, request
from peewee import *
from resp import *
from model import *
import re
import uuid
import datetime
import time

module = Blueprint('api_projects', __name__)


@module.route('/', methods=['GET'])
def list():
    return success(Project.select(), True);

@module.route('/<int:id>', methods=['GET'])
def show(id):

    try:
        return success(Project.get(id=id)._data)
    except Project.DoesNotExist:
        return error('Project does not exist', 404)

@module.route('/', methods=['POST'])
def create():

    if not request.json or not 'title' in request.json \
            or not 'content' in request.json \
            or not 'owner_id' in request.json \
            or not 'due_date' in request.json:
        return error('Missing title, content, owner_id or due_date')

    if not 'token' in request.json:
    	return error('Missing login token access')

    # Simple check name is valid or not
    if not re.match('^[^\s]+\s[^\s]', request.json['title']):
        return error('Name need to have 2 or more words')

    if not len(request.json['content'].split(' ')) > 5:
        return error('content must be longer more than 5 character')
    
    # calculate time

    current_timestamp = int(time.time())
    due_date_timestamp = int(time.mktime(datetime.datetime.strptime(request.json['due_date'], '%Y-%m-%d %H:%M:%S').timetuple()))

    if (due_date_timestamp < current_timestamp + 80600):
        return error('due_date must be greater than current time atleast 24h')

    try:
        user = User.get(token=request.json['token'])
        team = Team.get(id=request.json['owner_id'])

        if not team.leader == user:
            return error('You does not have permission to create project for this team')
        
        project = Project.create(title=request.json['title'],
            content=request.json['content'],
            due_date=request.json['due_date'])

        Owner.create(project=project, team=team)

        # Just hook team id to return data, refactor soon
        project._data['owner_id'] = team.id
        return success(project._data)

    except User.DoesNotExist:
        return error('Token login is incorrected')
    except Team.DoesNotExist:
    	return error('Team does not exists')


@module.route('/<int:id>', methods=['PUT'])
def update(id):
    pass


@module.route('/<int:id>', methods=['DELETE'])
def destroy(id):
    if not 'token' in request.json:
    	return error('Missing login token access')

    try:
        user = User.get(token=request.json['token'])
        project = Project.get(id=id)
        owner = Owner.get(project=project)
        if not user.id == owner.team.leader.id:
        	return error('You do not have permission for this action')

        Owner.delete().where(Owner.project == project).execute();
        Project.delete().where(Project.id == project.id).execute()
        return success('Delete success')
        
    except User.DoesNotExist:
        return error('Token login is incorrected')
    except Project.DoesNotExist:
    	return error('Project does not exist')
    except Owner.DoesNotExist:
        return error('Owner project does not exist')