from pony.orm import db_session, commit
from models import Careers

 
@db_session
def save_or_get_career(career_name:str):
    check_career = Careers.get(name=career_name)
    if check_career is not None:
        return check_career.ID
    else:
        career = Careers(name=career_name)
        commit()
        return career.ID