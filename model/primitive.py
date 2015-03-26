"""
This module to declare the basic model
We should refactor it when posible
"""
from base import *

class User(BaseModel):

    email = CharField(unique=True)
    password = CharField()
    token = CharField()


class Team(BaseModel):

    name = CharField()
    code = CharField(unique=True)
    leader = ForeignKeyField(User)


class Project(BaseModel):

    title = CharField()
    content = CharField()
    due_date = DateTimeField()


class Task(BaseModel):

    title = CharField()
    content = CharField()
    due_date = DateTimeField(null=True)
    project = ForeignKeyField(Project)


# Relationship models bellow

class Member(BaseModel):

    user = ForeignKeyField(User)
    task = ForeignKeyField(Task)


class Owner(BaseModel):

    team = ForeignKeyField(Team)
    project = ForeignKeyField(Project)


class Role(BaseModel):

    user = ForeignKeyField(User)
    team = ForeignKeyField(Team)
