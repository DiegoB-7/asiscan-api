from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from models import (Events,User)
from schemas import (
    events as events_schema
)
from modules import (
    auth as auth_module
)
from pony.orm import db_session, commit

router = APIRouter(
    prefix="/events",
    responses={404: {"description": "Not found"}},
)

@router.post("/create",status_code=status.HTTP_201_CREATED)
@db_session
def create_event(event:events_schema.event_in,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]) :
    event =  Events(
        name=event.name,
        user=current_user
    )
    
    return {
        "event": event.name,
    }

@router.get("")
@db_session
def get_events(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user = User.get(ID=current_user)
    data = []
    careerID = user.careerID
    
    users_by_career_id = User.select(lambda u: u.careerID == careerID)
    
    for user in users_by_career_id:
        for event in user.events:
            data.append({
                "ID": event.ID,
                "name": event.name,
                "user": event.user.firstName + " " + event.user.middleName + " " + event.user.lastName,
                "createdAt": datetime.datetime.strftime(event.createdAt, "%d/%m/%Y")
            })
    
    return data


