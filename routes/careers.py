from fastapi import APIRouter, HTTPException, status,Depends

from models import (Careers)

from schemas import (
    careers as careers_schema
)

from pony.orm import db_session, commit

router = APIRouter(
    prefix="/careers",
    responses={404: {"description": "Not found"}},
)

@router.get("",status_code=status.HTTP_200_OK)
@db_session
def get_careers():
    data = []
    careers = Careers.select()

    for career in careers:
        data.append({
            "id": career.ID,
            "name": career.name,

        })

    return data

##create career with pydantic schema
@router.post("/create",status_code=status.HTTP_201_CREATED)
@db_session
def create_career(career:careers_schema.career_in) :
    career =  Careers(
        name=career.name
    )

    return {
        "career": career.name,
    }


##verify if is career table empty
@router.get("/is_empty",status_code=status.HTTP_200_OK)
@db_session
def is_empty():
    careers = Careers.select()
    if careers:
        return False
    else:
        return True