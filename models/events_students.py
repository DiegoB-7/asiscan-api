from pony.orm import *
import time,datetime
from .events import Events
from .students import Students
from .users import User
from .base import db

class EventsStudents(db.Entity):
    ID = PrimaryKey(int, auto=True)
    event = Required(Events)
    student = Required(Students)
    quantity_assist = Required(int)
    user_id = Required(User)
    createdAt = Required(datetime.datetime,default=datetime.datetime.now)