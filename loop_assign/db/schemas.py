from pydantic import BaseModel
from datetime import datetime
from .models import StoreStatus


class StoreHoursBase(BaseModel):
    store_id: str
    timezone_str: str


class StoreHoursCreate(StoreHoursBase):
    pass


class StoreHours(StoreHoursBase):
    class Config:
        orm_mode = True


class StoreStatusBase(BaseModel):
    store_id: str
    timestamp_utc: datetime
    status: str


class StoreStatusCreate(StoreStatusBase):
    pass


class StoreStatus(StoreStatusBase):
    class Config:
        orm_mode = True


class StoresHoursScheduleBase(BaseModel):
    store_id: str
    dayOfWeek: int
    start_time_local: datetime
    end_time_local: datetime


class StoresHoursScheduleCreate(StoresHoursScheduleBase):
    pass


class StoresHoursSchedule(StoresHoursScheduleBase):
    class Config:
        orm_mode = True


class TriggerReportBase(BaseModel):
    report_id: str
    status: str
    progress: int


class TriggerReportCreate(TriggerReportBase):
    pass


class TriggerReport(TriggerReportBase):
    class Config:
        orm_mode = True
