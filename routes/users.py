from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
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

##is users table empty?
@router.get("/is_empty",status_code=status.HTTP_200_OK)
@db_session
def is_empty():
    users = User.select()
    if len(users) == 0:
        return True
    return False

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

    rol = 2

    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if(user.email=="admin@admin.tec"):
        rol = 1

    user =  User(
        firstName=user.firstName,
        middleName=user.middleName,
        lastName=user.lastName,
        careerID=user.careerID,
        rolID=rol,
        email=user.email,
        password=auth_module.hash_password(user.password),

    )
    user.flush()
    user_id = int(user.ID)

    return   {
        "access_token": auth_module.generate_token(user_id),
        "token_type": "bearer"
    }

@router.get("/{id:int}",status_code=status.HTTP_200_OK)
@db_session
def get_user(id:int,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user = User.get(ID=id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    data = {}
    for key in user.to_dict():
        if key != "password":
            if(key == "rolID"):
                data["rolID"] = user.rolID.ID
            elif(key == "careerID"):
                data["careerID"] = user.careerID.ID
            else:
                data[key] = user.to_dict()[key]
    return data

@router.get("",status_code=status.HTTP_200_OK)
@db_session
def get_all_users(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    users = User.select()
    data = []
    for user in users:
        data.append({
            "ID": user.ID,
            "name": user.firstName + " " + user.middleName + " " + user.lastName,
            "career": user.careerID.name,
            "rol": user.rolID.name,
            "email": user.email,
            "createdAt": datetime.datetime.strftime(user.createdAt, "%d/%m/%Y")
        })
    return data

@router.delete("/{id}",status_code=status.HTTP_200_OK)
@db_session
def delete_user(id:int,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user_check = User.get(ID=id)

    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if id == current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't delete yourself",
        )

    user = User[id]
    user.delete()
    commit()
    return {"message":"User deleted"}

@router.put("/{id}",status_code=status.HTTP_200_OK)
@db_session
def update_user(id:int,user:users_schema.user_in_update, current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user_check = User.get(ID=id)

    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_database = User[id]

    if user.password:
        user_database.set(
            firstName=user.firstName,
            middleName=user.middleName,
            lastName=user.lastName,
            careerID=user.careerID,
            rolID=user.rolID,
            email=user.email,
            password=auth_module.hash_password(user.password),

        )
    else:
        user_database.set(
            firstName=user.firstName,
            middleName=user.middleName,
            lastName=user.lastName,
            careerID=user.careerID,
            rolID=user.rolID,
            email=user.email,

        )

    commit()

    return {"message":"User updated"}

@router.get("/me",status_code=status.HTTP_200_OK)
@db_session
def get_profile_information(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
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