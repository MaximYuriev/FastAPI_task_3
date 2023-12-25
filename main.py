from fastapi import FastAPI
import uvicorn
from fastapi.responses import PlainTextResponse
from datetime import datetime
from public.hospital import hospital_router
from public.db import create_tables

#create_tables()

app = FastAPI()
app.include_router(hospital_router)
@app.on_event("startup")
def on_startup():
    open("log_p.txt", mode = "a").write(f'{datetime.utcnow()}: Begin\n')
@app.on_event("shutdown")
def shutdown():
    open("log_p.txt",mode = "a").write(f'{datetime.utcnow()}: End\n')

@app.get('/',response_class=PlainTextResponse)
def f_indexH():
    return"<b> Hello! </b>"
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = 8000)