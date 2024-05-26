from pony.orm import *
import time,datetime
from .users import User    
from .base import db

class Events(db.Entity):
    ID = PrimaryKey(int, auto=True)
    name = Required(str)
    user = Required(User)
    events_students = Set('EventsStudents')
    createdAt = Required(datetime.datetime,default=datetime.datetime.now)