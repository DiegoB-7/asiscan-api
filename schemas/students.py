from pydantic import BaseModel,EmailStr
 
class student_in(BaseModel):
    firstName: str
    middleName: str
    lastName: str
    controlNumber:str
    careerID: int
    email: EmailStr
   