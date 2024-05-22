from fastapi import APIRouter, HTTPException, status,Depends

from models import (Careers)


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