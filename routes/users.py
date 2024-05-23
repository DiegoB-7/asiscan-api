from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import (User)
from schemas import (
    users as users_schema
)
from modules import (
    auth as auth_module
)
from pony.orm import db_session, commit

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.post("/sign_in",status_code=status.HTTP_200_OK)
@db_session
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    check_user = User.get(email=form_data.username)
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not auth_module.hash_password(form_data.password) == check_user.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password",
        )
    user_id = int(check_user.ID)
    
    return {
        "access_token": auth_module.generate_token(user_id),
        "token_type": "bearer"
    }
    
@router.post("/sign_up",status_code=status.HTTP_201_CREATED)
@db_session
def sign_up(user:users_schema.user_in) :
    check_user = User.get(email=user.email)
    
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user =  User(
        firstName=user.firstName,
        middleName=user.middleName,
        lastName=user.lastName,
        careerID=user.careerID,
        rolID=2,
        email=user.email,
        password=auth_module.hash_password(user.password),
        
    )
    user.flush() 
    user_id = int(user.ID)
    
    return   {
        "access_token": auth_module.generate_token(user_id),
        "token_type": "bearer"
    }

@router.get("/me",status_code=status.HTTP_200_OK)
@db_session
def me(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    data = {}
    user = User.get(ID=current_user)
    
    for key in user.to_dict():
        if key != "password":
            if(key == "rolID"):
                data["rol"] = user.rolID.name
            elif(key == "careerID"):
                data["career"] = user.careerID.name
            else:
                data[key] = user.to_dict()[key]

    return data

@router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
@db_session
def delete_user(id:int,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user_check = User.get(ID=id)
    
    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = User[id]
    user.delete()
    commit()
    return {"message":"User deleted"}

@router.put("/edit/{id}",status_code=status.HTTP_200_OK)
@db_session
def edit_user(id:int,user:users_schema.user_in, current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user_check = User.get(ID=id)

    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    user_database = User[id]
   
    user_database.set(
        firstName=user.firstName,
        middleName=user.middleName,
        lastName=user.lastName,
        careerID=user.careerID,
        rolID=user.rolID,
        email=user.email,
        password=auth_module.hash_password(user.password),
        avatar=user.avatar
    )
    
    commit()
   
    return {"message":"User updated"}