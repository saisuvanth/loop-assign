from sqlalchemy.orm import Session

from . import models, schemas


def create_store_hours(db: Session, store_hours: schemas.StoreHoursCreate):
    db_store_hours = models.StoreHours(
        store_id=store_hours.store_id, timezone_str=store_hours.timezone_str)
    db.add(db_store_hours)
    db.commit()
    db.refresh(db_store_hours)
    return db_store_hours


def create_store_status(db: Session, store_status: schemas.StoreStatusCreate):
    db_store_status = models.StoreStatus(
        store_id=store_status.store_id, timestamp_utc=store_status.timestamp_utc, status=store_status.status)
    db.add(db_store_status)
    db.commit()
    db.refresh(db_store_status)
    return db_store_status


def create_store_hours_schedule(db: Session, store_hours_schedule: schemas.StoresHoursScheduleCreate):
    db_store_hours_schedule = models.StoresHoursSchedule(
        store_id=store_hours_schedule.store_id, dayOfWeek=store_hours_schedule.dayOfWeek, start_time_local=store_hours_schedule.start_time_local, end_time_local=store_hours_schedule.end_time_local)
    db.add(db_store_hours_schedule)
    db.commit()
    db.refresh(db_store_hours_schedule)
    return db_store_hours_schedule


def create_report(db: Session, report: schemas.TriggerReportCreate):
    db_report = models.TriggerReport(
        report_id=report.report_id, status=report.status)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report_progress(db: Session, report_id: str):
    res = db.query(models.TriggerReport).filter(
        models.TriggerReport.report_id == report_id).first()
    print(str(res))
    return res


def update_report(db: Session, report_id: str, status: models.TriggerReportStatus, progress: int):
    db.query(models.TriggerReport).filter(
        models.TriggerReport.report_id == report_id).update({'status': status, 'progress': progress})
    db.commit()
