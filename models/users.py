from pony.orm import *
import time,datetime
from .base import db
from .rols import Rols
from .careers import Careers

class User(db.Entity):
    ID = PrimaryKey(int, auto=True)
    firstName = Required(str)
    middleName = Required(str)
    lastName = Required(str)
    email = Required(str)
    password = Required(str)
    careerID = Required(Careers)
    rolID= Required(Rols)
    createdAt = Required(datetime.datetime,default=datetime.datetime.now)
    events = Set('Events')
    events_students = Set('EventsStudents') 
    
    
    
