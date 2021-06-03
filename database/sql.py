from peewee import *
import datetime
import os

db_name = 'test.db'
db_exists = False
if os.path.exists('database/data/' + db_name):
    db_exists = True

db = SqliteDatabase('database/data/' + db_name)


class BaseModel(Model):
    class Meta:
        database = db


class Topics(BaseModel):
    name = TextField()
    plaintext = TextField()


class Courses(BaseModel):
    name = TextField()
    plaintext = TextField()
    topic = ForeignKeyField(Topics)
    approved = BooleanField(default=False)


class Teachers(BaseModel):
    first_name = TextField()
    last_name = TextField()


class Classes(BaseModel):
    course = ForeignKeyField(Courses)
    teacher = ForeignKeyField(Teachers)
    period = IntegerField()
    approved = BooleanField(default=False)


class Work(BaseModel):
    from_class = ForeignKeyField(Classes)
    created_on = DateField(default=datetime.datetime.now())
    due_by = DateField(default=datetime.datetime.now())
    name = TextField()
    description = TextField()
    url = TextField()


if not db_exists:
    print('Database doesn\'t exist, creating now!')
    db.connect()
    db.create_tables([Topics, Courses, Teachers, Classes, Work])
    Topics.create(name='Math', plaintext='math')
    Topics.create(name='English', plaintext='english')
