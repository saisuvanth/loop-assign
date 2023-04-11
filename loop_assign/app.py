from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from db import crud, models, schemas, engine, SessionLocal
from utils.schemas import TriggerResponse
from utils.report import make_report
from sqlalchemy.orm import Session
import uuid
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
                   '*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event('startup')
async def startup_event():
    print('startup event')


@app.get('/')
def index():
    return {'message': 'PONG!'}


@app.post('/trigger_report', response_model=TriggerResponse)
def trigger_report(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    report_id = str(uuid.uuid4())
    rs = crud.create_report(db=db, report=schemas.TriggerReportCreate(
        report_id=report_id, status='pending', progress=0))
    background_tasks.add_task(make_report, report_id, db)
    return {'report_id': report_id}


@app.get('/get-report')
async def get_report(report_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = crud.get_report_progress(db=db, report_id=report_id)
    if (res and res.status == models.TriggerReportStatus.success):
        background_tasks.add_task(os.remove, 'reports/'+report_id+'.csv')
        return FileResponse('reports/'+report_id+'.csv')
    elif (res and res.status == models.TriggerReportStatus.pending):
        return {'status': 'pending', 'progress': f'{res.progress}%'}
    else:
        return {'message': 'report not found'}
