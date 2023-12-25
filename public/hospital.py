from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from typing import Union, Annotated
from sqlalchemy.orm import Session
from public.db import engine_s
from models.good import *


def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()

hospital_router = APIRouter( prefix='/api/hospital')
#Работа с таблицами, содержащими информацию о пациентах
@hospital_router.get("/doctor/{id}",response_model = Union[New_Respons, Main_Doctor], tags=[Tags.doctor] )
def get_doctor_(id: int, DB: Session = Depends(get_session)):
    doctor = DB.query(Doctor).filter(Doctor.id == id).first()
    if doctor == None:
        return JSONResponse(status_code=404, content={"message": "Врач не найден"})
    else:
        return doctor

@hospital_router.get("/doctor", response_model = Union[list[Main_Doctor], New_Respons],tags=[Tags.doctor])
def get_doctor_db(DB: Session = Depends(get_session)):
    doctors = DB.query(Doctor).all()
    if doctors == None:
        return JSONResponse(status_code= 404, content={"message": "Врачи не найдены"})
    return doctors

@hospital_router.post("/doctor",response_model=Union[Main_Doctor, New_Respons],tags=[Tags.doctor],status_code=status.HTTP_201_CREATED)
def create_doctor(item: Annotated[Main_Doctor,Body(embed = True, description="Новый врач")],DB: Session = Depends(get_session)):
    try:
        doctor = Doctor(surname= item.surname,name = item.name,patronymic = item.patronymic)
        if doctor is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(doctor)
        DB.commit()
        DB.refresh(doctor)
        return doctor
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта {doctor}")

@hospital_router.put("/doctor", response_model=Union[Main_Doctor, New_Respons], tags=[Tags.doctor])
def edit_person(item: Annotated[Main_Doctor,Body(embed = True, description="Изменение данных врача по id")], DB: Session = Depends(get_session)):
    doctor = DB.query(Doctor).filter(Doctor.id == item.id).first()
    if doctor == None:
        return JSONResponse(status_code= 404, content={"message": "Врач не найден"})
    doctor.surname = item.surname
    doctor.name = item.name
    doctor.patronymic = item.patronymic
    try:
        DB.commit()
        DB.refresh(doctor)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})

@hospital_router.delete("/doctor/{id}",response_class=JSONResponse,tags=[Tags.doctor])
def delete_person(id: int, DB: Session = Depends(get_session)):
    doctor = DB.query(Doctor).filter(Doctor.id == id).first()
    if doctor == None:
        return JSONResponse(status_code=404,content={"message": "Врач не найден"})
    try:
        DB.delete(doctor)
        DB.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Ошибка'})
    return JSONResponse(content={'message': f'Врач удален {id}'})


@hospital_router.patch("/doctor/{id}", response_model=Union[Main_Doctor, New_Respons], tags=[Tags.doctor])
def edit_doctor(id: int, item: Annotated[Main_Doctor, Body(embed=True, description="Изменяем данные по id")], DB: Session = Depends(get_session)):
    doctor = DB.query(Doctor).filter(Doctor.id == id).first()
    if doctor == None:
        return JSONResponse(status_code=404, content={"message": "Доктор не найден"})
    if item.surname != "" and item.surname is not None:
        doctor.surname = item.surname
    if item.name != "" and item.name is not None:
        doctor.name = item.name
    if item.patronymic != "" and item.patronymic is not None:
        doctor.patronymic = item.patronymic
    try:
        DB.commit()
        DB.refresh(doctor)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})


#Работа с таблицами, содержащими информацию о пациентах
@hospital_router.get("/patient/{id}",response_model = Union[New_Respons, Main_Patient], tags=[Tags.patient] )
def get_patient_(id: int, DB: Session = Depends(get_session)):
    patient = DB.query(Patient).filter(Patient.id == id).first()
    if patient == None:
        return JSONResponse(status_code=404, content={"message": "Пациент не найден"})
    else:
        return patient

@hospital_router.get("/patient", response_model = Union[list[Main_Patient], New_Respons],tags=[Tags.patient])
def get_patient_db(DB: Session = Depends(get_session)):
    patients = DB.query(Patient).all()
    if patients == None:
        return JSONResponse(status_code= 404, content={"message": "Пациенты не найдены"})
    return patients

@hospital_router.post("/patient",response_model=Union[Main_Patient, New_Respons],tags=[Tags.patient],status_code=status.HTTP_201_CREATED)
def create_patient(item: Annotated[Main_Patient,Body(embed = True, description="Новый пациент")],DB: Session = Depends(get_session)):
    try:
        patient = Patient(surname= item.surname,name = item.name,patronymic = item.patronymic, passport = item.passport)
        if patient is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(patient)
        DB.commit()
        DB.refresh(patient)
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта {patient}")

@hospital_router.put("/patient", response_model=Union[Main_Patient, New_Respons], tags=[Tags.patient])
def edit_person(item: Annotated[Main_Patient,Body(embed = True, description="Изменение данных пациента по id")], DB: Session = Depends(get_session)):
    patient = DB.query(Patient).filter(Patient.id == item.id).first()
    if patient == None:
        return JSONResponse(status_code= 404, content={"message": "Пациент не найден"})
    patient.surname = item.surname
    patient.name = item.name
    patient.patronymic = item.patronymic
    patient.passport = item.passport
    try:
        DB.commit()
        DB.refresh(patient)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})

@hospital_router.delete("/patient/{id}",response_class=JSONResponse,tags=[Tags.patient])
def delete_person(id: int, DB: Session = Depends(get_session)):
    patient = DB.query(Patient).filter(Patient.id == id).first()
    if patient == None:
        return JSONResponse(status_code=404,content={"message": "Пациент не найден"})
    try:
        DB.delete(patient)
        DB.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Ошибка'})
    return JSONResponse(content={'message': f'Пациент удален {id}'})

@hospital_router.patch("/patient/{id}", response_model=Union[Main_Patient, New_Respons], tags= [Tags.patient])
def edit_patient(id: int, item: Annotated[Main_Patient, Body(embed= True,description="Изменяем данные по id")], DB: Session = Depends(get_session)):
    patient = DB.query(Patient).filter(Patient.id == id).first()
    if patient == None:
        return JSONResponse(status_code=404, content={"message": "Пациент не найден"})
    if item.surname != "" and item.surname is not None:
        patient.surname = item.surname
    if item.name != "" and item.name is not None:
        patient.name = item.name
    if item.patronymic != "" and item.patronymic is not None:
        patient.patronymic = item.patronymic
    if item.passport != "" and item.passport is not None:
        patient.passport = item.passport
    try:
        DB.commit()
        DB.refresh(patient)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":""})

#История болезни
@hospital_router.get("/history/{id}",response_model = Union[New_Respons, Main_History], tags=[Tags.history] )
def get_history_(id: int, DB: Session = Depends(get_session)):
    history = DB.query(DiseaseHistory).filter(DiseaseHistory.id == id).first()
    if history == None:
        return JSONResponse(status_code=404, content={"message": "Запись не найдена"})
    else:
        return history

@hospital_router.get("/history", response_model = Union[list[Main_History], New_Respons],tags=[Tags.history])
def get_history_db(DB: Session = Depends(get_session)):
    history = DB.query(DiseaseHistory).all()
    if history == None:
        return JSONResponse(status_code= 404, content={"message": "Записи не найдены"})
    return history

@hospital_router.post("/history",response_model=Union[Main_History, New_Respons],tags=[Tags.history],status_code=status.HTTP_201_CREATED)
def create_history(item: Annotated[Main_Patient,Body(embed = True, description="Новая запись")],DB: Session = Depends(get_session)):
    try:
        history = DiseaseHistory(id_doctor= item.id_doctor,id_patient = item.id_patient,diagnosis = item.diagnosis)
        if history is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(history)
        DB.commit()
        DB.refresh(history)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта {history}")

@hospital_router.put("/history", response_model=Union[Main_History, New_Respons], tags=[Tags.history])
def edit_history(item: Annotated[Main_Patient,Body(embed = True, description="Изменение данных по id")], DB: Session = Depends(get_session)):
    history = DB.query(DiseaseHistory).filter(DiseaseHistory.id == item.id).first()
    if history == None:
        return JSONResponse(status_code= 404, content={"message": "Запись не найдена"})
    history.id_doctor = item.id_doctor
    history.id_patient = item.id_patient
    history.diagnosis = item.diagnosis
    try:
        DB.commit()
        DB.refresh(history)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})

@hospital_router.delete("/history/{id}",response_class=JSONResponse,tags=[Tags.history])
def delete_history(id: int, DB: Session = Depends(get_session)):
    history = DB.query(DiseaseHistory).filter(DiseaseHistory.id == id).first()
    if history == None:
        return JSONResponse(status_code=404,content={"message": "Запись не найдена"})
    try:
        DB.delete(history)
        DB.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Ошибка'})
    return JSONResponse(content={'message': f'Запись удалена {id}'})

@hospital_router.patch("/history/{id}", response_model=Union[Main_History, New_Respons], tags= [Tags.history])
def edit_history(id: int,item: Annotated[Main_History, Body(embed= True,description="Изменяем данные по id")], DB: Session = Depends(get_session)):
    history = DB.query(DiseaseHistory).filter(DiseaseHistory.id == id).first()
    if history == None:
        return JSONResponse(status_code=404, content={"message": "Запись не найдена"})
    if item.id_doctor is not None:
        history.id_doctor = item.id_doctor
    if item.id_patient is not None:
        history.id_patient = item.id_patient
    if item.diagnosis != "" and item.diagnosis is not None:
        history.diagnosis = item.diagnosis
    try:
        DB.commit()
        DB.refresh(history)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":""})