from config import settings
from sqlalchemy import create_engine, text
from models.good import Base

ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA
print(ur_s)
engine_s = create_engine(ur_s,echo= True)

def create_tables():
    Base.metadata.drop_all(bind= engine_s)
    Base.metadata.create_all(bind= engine_s)

