from model import *;

database.connect()
database.create_tables([User, Team, Project, Task, Member, Owner, Role])
