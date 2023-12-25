from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Identity, ForeignKey
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()
class Doctor(Base):
    __tablename__ = 'Doctor'
    id = Column(Integer, Identity(start= 1),primary_key=True)
    surname = Column(String, nullable=False) #фамилия
    name = Column(String,nullable= False) #имя
    patronymic = Column(String, nullable=False) #отчество

class Patient(Base):
    __tablename__ = 'Patient'
    id = Column(Integer, Identity(start= 1),primary_key=True)
    surname = Column(String, nullable=False) #фамилия
    name = Column(String,nullable= False) #имя
    patronymic = Column(String, nullable=False) #отчество
    passport = Column(String, nullable=False)  # паспортные данные

class DiseaseHistory(Base):
    __tablename__ = 'DiseaseHistory'
    id = Column(Integer, Identity(start=1), primary_key=True)
    id_doctor = Column(Integer, ForeignKey(Doctor.id),nullable= False)
    id_patient = Column(Integer, ForeignKey(Patient.id),nullable= False)
    diagnosis = Column(String,nullable= False)

class New_Respons(BaseModel):
    message: str

class Main_Doctor(BaseModel):
    id: int
    surname: str
    name: str
    patronymic:str

class Main_Patient(BaseModel):
    id: int
    surname: str
    name: str
    patronymic: str
    passport: str

class Main_History(BaseModel):
    id: int
    id_doctor: int
    id_patient: int
    diagnosis: str

class Tags(Enum):
    hospital = "Hospital"
    doctor = "Doctor"
    patient = "Patient"
    history = "DiseaseHistory"