from flask import Blueprint, abort, jsonify, request
from peewee import *
from resp import *
import re
import uuid
from model import *

module = Blueprint('api_teams', __name__)


@module.route('/', methods=['GET'])
def list():
    return success(Team.select(), True)

@module.route('/<id>', methods=['GET'])
def show(id):
    try:
        return success(Team.get(id=id)._data)
    except Team.DoesNotExist:
        return error('Team does not exist', 404)

@module.route('/', methods=['POST'])
def create():
    if not request.json or not 'name' in request.json or not 'code' in request.json:
        return error('Missing email or password')

    if not 'token' in request.json:
    	return error('Missing login token access')

    # Simple check name is valid or not
    if not re.match('^[^\s]+\s[^\s]', request.json['name']):
        return error('Name need to have 2 or more words')

    try:
        user = User.get(token=request.json['token'])
        team = Team.create(name=request.json['name'], code=request.json['code'], leader=user)
        Role.create(user=user, team=team)
    except User.DoesNotExist:
        return error('Token login is incorrected')
    except IntegrityError:
    	return error('Code is duplicate')

    return success(team._data)


@module.route('/<int:id>', methods=['PUT'])
def update(id):
    pass


@module.route('/<int:id>', methods=['DELETE'])
def destroy(id):
    if not 'token' in request.json:
    	return error('Missing login token access')

    try:
        user = User.get(token=request.json['token'])
        team = Team.get(id=id)
        if not user.id == team.leader.id:
        	return error('You do not have permission for this action')

        Role.delete().where(Role.team == team).execute();
        Team.delete().where(Team.id == team.id).execute()
        return success('Delete success')
        
    except User.DoesNotExist:
        return error('Token login is incorrected')
    except Team.DoesNotExist:
    	return error('Team does not exist')