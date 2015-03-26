from flask import Blueprint, abort, jsonify, request
from peewee import *
from resp import *
from model import *
import re
import uuid
import datetime
import time

module = Blueprint('api_tasks', __name__)


@module.route('/', methods=['GET'])
def list():
    return success(Task.select(), True)

@module.route('/<int:id>', methods=['GET'])
def show(id):
    try:
        return success(Task.get(id=id)._data)
    except Task.DoesNotExist:
        return error('Task does not exist', 404)

@module.route('/', methods=['POST'])
def create():
    if not request.json or not 'title' in request.json \
            or not 'content' in request.json \
            or not 'project_id' in request.json:
        return error('Missing title, content, project_id')

    if not 'token' in request.json:
    	return error('Missing login token access')

    # Simple check name is valid or not
    if not re.match('^[^\s]+\s[^\s]', request.json['title']):
        return error('Name need to have 2 or more words')
    if not len(request.json['content'].split(' ')) > 5:
        return error('content must be longer more than 5 character')

    try:
        user = User.get(token=request.json['token'])
        project = Project.get(id=request.json['project_id'])
        owner = Owner.get(project=project)
        
        # Everyone can create tasks?
        
        task = Task.create(title=request.json['title'],
                content=request.json['content'],
                project=project)

        # Just hook team id to return data, refactor soon
        # project._data['owner_id'] = owner.team.id
        return success({'id': task.id, 'name': owner.team.name, 'code': owner.team.code, 'lead_id': owner.team.leader.id})

    except User.DoesNotExist:
        return error('Token login is incorrected')
    except Project.DoesNotExist:
    	return error('Project does not exists')


@module.route('/<int:id>', methods=['PUT'])
def update(id):
    pass


@module.route('/<int:id>', methods=['DELETE'])
def destroy(id):
    if not 'token' in request.json:
    	return error('Missing login token access')

    try:
        user = User.get(token=request.json['token'])
        task = Task.get(id=id)
        owner = Owner.get(project=task.project)
        if not user.id == owner.team.leader.id:
        	return error('You do not have permission for this action')

        Member.delete().where(Member.task == task).execute();
        Task.delete().where(Task.id == task.id).execute()
        return success('Delete success')
        
    except User.DoesNotExist:
        return error('Token login is incorrected')
    except Project.DoesNotExist:
    	return error('Project does not exist')
    except Owner.DoesNotExist:
        return error('Owner project does not exist')



# Additional resource
@module.route('/<int:id>/members', methods=['POST'])
def add_members(id):
    if not 'members' in request.json:
        return errors('Members is required')

    try:
        user = User.get(token=request.json['token'])
        task = Task.get(id=id)
        for member in request.json['members']:
            Member.create(task=task, user=member)
        return success('Add members success')
    except User.DoesNotExist:
        return error('Token login is incorrected')
    except Task.DoesNotExist:
        return error('Task does not exists')