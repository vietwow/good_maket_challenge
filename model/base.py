from peewee import *


# Hard code is suck, we should refactor it soon
database = psql_db = PostgresqlDatabase('inori', user='postgres', password='khongbiet')

class BaseModel(Model):

    class Meta:
        database = database;
