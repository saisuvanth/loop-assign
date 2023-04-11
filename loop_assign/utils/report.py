import pytz
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db import models, crud
import csv
import os


def get_uptime_downtime(store_id: str, db: Session, start_time, end_time):
    statuses = db.query(models.StoreStatus).filter(models.StoreStatus.store_id == store_id,
                                                   models.StoreStatus.timestamp_utc >= start_time,
                                                   models.StoreStatus.timestamp_utc <= end_time,
                                                   ).all()
    total_uptime = timedelta()
    total_downtime = timedelta()
    prev_status = None
    for status in statuses:
        if prev_status is not None:
            time_diff = status.timestamp_utc-prev_status.timestamp_utc
            if prev_status.status == models.StoreStatusEnum.active:
                total_uptime += time_diff
            else:
                total_downtime += time_diff
        prev_status = status
    return total_uptime.total_seconds(), total_downtime.total_seconds()


def make_report(report_id: str, db: Session):
    stores = db.query(models.StoreHours).limit(500).all()
    now = datetime.now()
    # get time for last hour, day, week
    last_hour = now - timedelta(hours=1)
    last_day = now - timedelta(days=1)
    last_week = now - timedelta(weeks=1)
    interpolated_data = []
    prev_progress = 0
    for index, store in enumerate(stores):
        timezone = pytz.timezone(store.timezone_str)
        startime_utc = timezone.localize(last_hour).astimezone(pytz.utc)
        endtime_utc = timezone.localize(now).astimezone(pytz.utc)
        # localize the time to the store's timezone and get uptime and downtime
        uptime_last_hour, downtime_last_hour = (get_uptime_downtime(
            store.store_id, db, startime_utc, endtime_utc))
        startime_utc = timezone.localize(last_day).astimezone(pytz.utc)
        endtime_utc = timezone.localize(now).astimezone(pytz.utc)
        uptime_last_day, downtime_last_day = (get_uptime_downtime(
            store.store_id, db, startime_utc, endtime_utc))
        startime_utc = timezone.localize(last_week).astimezone(pytz.utc)
        endtime_utc = timezone.localize(now).astimezone(pytz.utc)
        uptime_last_week, downtime_last_week = (get_uptime_downtime(
            store.store_id, db, startime_utc, endtime_utc))
        # get minutes from seconds
        uptime_last_hour = uptime_last_hour/60
        downtime_last_hour = downtime_last_hour/60
        # get hours from seconds
        uptime_last_day = uptime_last_day/3600
        uptime_last_week = uptime_last_week/3600
        downtime_last_day = downtime_last_day/3600
        downtime_last_week = downtime_last_week/3600
        interpolated_data.append([
            store.store_id,
            int(uptime_last_hour),
            int(downtime_last_hour),
            uptime_last_day,
            downtime_last_day,
            uptime_last_week,
            downtime_last_week
        ])
        cur_progress = int((index+1)/len(stores)*100)
        if cur_progress != prev_progress:
            prev_progress = cur_progress
            crud.update_report(
                db, report_id, models.TriggerReportStatus.pending, cur_progress)
    os.makedirs('reports', exist_ok=True)
    file = open(f'reports/{report_id}.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['store_id', 'uptime_last_hour', 'downtime_last_hour', 'uptime_last_day',
                     'downtime_last_day', 'uptime_last_week', 'downtime_last_week'])
    writer.writerows(interpolated_data)
    file.close()
    crud.update_report(db, report_id, models.TriggerReportStatus.success, 100)
