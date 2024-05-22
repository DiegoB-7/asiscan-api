from pydantic import BaseModel,EmailStr
 
class user_in(BaseModel):
    firstName: str
    middleName: str
    lastName: str
    careerID: int
    
    email: EmailStr
    password: str
    
    
class user_out(BaseModel):
    id: int
    firstName: str
    middleName: str
    lastName: str
    careerID: int
    rolID: int
    email: EmailStr
    avatar: str

class sign_up_out(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        orm_mode = True