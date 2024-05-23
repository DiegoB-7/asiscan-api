from models import db
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from routes import (
    users_router,
    careers_router,
    events_router
)
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
origins = ['*']

db.bind(provider='mysql', host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), passwd=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'))
db.generate_mapping(create_tables=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(careers_router)
app.include_router(events_router)



