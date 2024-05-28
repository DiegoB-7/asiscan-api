from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import datetime
from models import (Events,Students,EventsStudents,User)
from schemas import (
    students as students_schema
)
from modules import (
    students as students_module,
    careers as careers_module,
    auth as auth_module
)
from pony.orm import db_session, commit

router = APIRouter(
    prefix="/students",
    responses={404: {"description": "Not found"}},
)

@router.post("/save_assistance/{eventID}",status_code=status.HTTP_200_OK)
@db_session
def get_student_info(url:str,eventID:int,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    student_data = students_module.get_student_data_by_url(url)
    
    career_id = careers_module.save_or_get_career(student_data["career"])      
    student = Students.get(controlNumber=student_data["control_number"])

    if(student is None):  
        student = Students(
            firstName=student_data["first_name"],
            middleName=student_data["middle_name"],
            lastName=student_data["last_name"],
            email="",
            controlNumber=student_data["control_number"],
            careerID=career_id
        )
        commit()
    
    event =  Events.get(ID=eventID)
        
    assitance = EventsStudents.get(student=student.ID,event=event.ID)
        
    if assitance is None:
        assitance = EventsStudents(
                student=student.ID,
                event=event.ID,
                user_id=current_user,
                quantity_assist=1
        )
        commit()
    else:
        assitance.quantity_assist += 1
        commit()
            
    return student_data

@router.post("/create",status_code=status.HTTP_201_CREATED)
@db_session
def create_student(student:students_schema.student_in):
    
    check_student = Students.get(controlNumber=student.controlNumber)
    
    if check_student is not None:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    student = Students(
        firstName=student.firstName,
        middleName=student.middleName,
        lastName=student.lastName,
        email=student.email,
        controlNumber=student.controlNumber,
        careerID=student.careerID
    )
    
    return {
        "first_name": student.firstName,
        "middle_name": student.middleName,
        "last_name": student.lastName,
        "career": student.careerID.name,
    }

@router.get("",status_code=status.HTTP_200_OK)
@db_session
def get_students(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user = User.get(ID=current_user)
    data = []
    careerID = user.careerID
    print(careerID)
    students = Students.select(lambda s: s.careerID == careerID)
    
    for student in students:
        data.append({
            "ID": student.ID,
            "firstName": student.firstName,
            "middleName": student.middleName,
            "lastName": student.lastName,
            "controlNumber": student.controlNumber,
            "career": student.careerID.name
        })
    
    return data

@router.post("/save_assistance",status_code=status.HTTP_201_CREATED)
@db_session
def create_student(control_number:str,eventID:int,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    
    student = Students.get(controlNumber=control_number)
    
    if student is  None:
        raise HTTPException(status_code=400, detail="Student not found")

    event =  Events.get(ID=eventID)
    
    assitance = EventsStudents.get(student=student.ID,event=event.ID)
    
    if assitance is None:
        assitance = EventsStudents(
                student=student.ID,
                event=event.ID,
                user_id=current_user,
                quantity_assist=1
        )
        commit()
    else:
        assitance.quantity_assist += 1
        commit()
    
    return {
        "first_name": student.firstName,
        "middle_name": student.middleName,
        "last_name": student.lastName,
        "career": student.careerID.name,
    }
   

    