from pony.orm import *
import time,datetime
from .base import db
from .careers import Careers

class Students(db.Entity):
    ID = PrimaryKey(int, auto=True)
    firstName = Required(str)
    middleName = Required(str)
    lastName = Required(str)
    email = Optional(str)
    controlNumber = Required(str)
    careerID = Required(Careers)
    events_students = Set('EventsStudents')
    createdAt = Required(datetime.datetime,default=datetime.datetime.now)