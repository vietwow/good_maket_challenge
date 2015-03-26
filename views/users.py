from flask import Blueprint, abort, jsonify, request
from peewee import *
from resp import *
import re
import uuid
from model import User

module = Blueprint('api_users', __name__)


@module.route('/', methods=['GET'])
def list():
    
    result_list = []
    for user in User.select():
        result_list.append({'email': user.email, 'id': user.id})
    return success(result_list)

@module.route('/<int:id>', methods=['GET'])
def show(id):
    try:
        user = User.get(id=id)
        return success({'email': user.email, 'id': user.id})
    except User.DoesNotExist:
        return error('User does not exist', 404)

@module.route('/', methods=['POST'])
def create():
    if not request.json or not 'email' in request.json or not 'password' in request.json:
        return error('Missing email or password')

    # Simple check email is valid or not
    if not re.match('[^@]+@[^@]+\.[^@]+', request.json['email']):
        return error('Email is invalid')

    # Simple check password's length must be 6 chars or more
    if len(request.json['password']) < 6:
        return error('Password length must be 6 chars or greater')

    # Generate token
    token = uuid.uuid4()

    try:
        user = User.create(email=request.json['email'], password=request.json['password'], token=token)
    except IntegrityError as e:
        return error('Email is duplicate')

    return success({'token': token})


@module.route('/<id>', methods=['PUT'])
def update(id):
    pass


@module.route('/<id>', methods=['DELETE'])
def destroy(id):
    pass


# Additional user resource

@module.route('.json', methods=['POST'])
def login():
    if not request.json or not 'email' in request.json or not 'password' in request.json:
        return error('Login required username & password')

    try:
        user = User.get(email=request.json['email'])
        if not user.password == request.json['password']:
            return error('Password not match')
    except User.DoesNotExist:
        return error('Email does not exist')

    # Make a new token for user
    user.token = uuid.uuid4()
    user.save()

    return success({'token': user.token})
