from fastapi import APIRouter, HTTPException, status,Depends

from models import (Careers,Rols)


from schemas import (rol_in as rol_in_schema)

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

##create rol
@router.post("/create",status_code=status.HTTP_201_CREATED)
@db_session
def create_rol(rol_in: rol_in_schema):
    rol = Rols(name=rol_in.name)
    commit()
    return {
        "id": rol.ID,
        "name": rol.name,
    }

##is_empty the rols table?
@router.get("/is_empty",status_code=status.HTTP_200_OK)
@db_session
def is_empty():
    rols = Rols.select()
    if rols:
        return False
    else:
        return True