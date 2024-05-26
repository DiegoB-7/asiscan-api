from pony.orm import *
import time,datetime
from .base import db

class Careers(db.Entity):
    ID = PrimaryKey(int, auto=True)
    name = Required(str)
    user = Set('User')
    student = Set('Students')
