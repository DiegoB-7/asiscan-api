from fastapi import APIRouter, HTTPException, status,Depends

from models import (Careers,Rols)


from pony.orm import db_session, commit

router = APIRouter(
    prefix="/rols",
    responses={404: {"description": "Not found"}},
)

@router.get("",status_code=status.HTTP_200_OK)
@db_session
def get_rols():
    data = []
    rols = Rols.select()
    
    for rol in rols:
        data.append({
            "id": rol.ID,
            "name": rol.name,
            
        })
    
    return data