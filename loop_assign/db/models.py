import enum
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, String, event, Time
from sqlalchemy.orm import relationship, sessionmaker
from . import Base


class StoreStatusEnum(enum.Enum):
    active = 'active'
    inactive = 'inactive'


class TriggerReportStatus(enum.Enum):
    success = 'success'
    pending = 'pending'


class StoreHours(Base):
    __tablename__ = 'store_hours'

    store_id = Column(String, primary_key=True)
    timezone_str = Column(String(50), nullable=False)

    schedule = relationship('StoresHoursSchedule', back_populates='store')
    statuses = relationship('StoreStatus', back_populates='store')


class StoreStatus(Base):
    __tablename__ = 'store_status'

    store_id = Column(String, ForeignKey(
        'store_hours.store_id'), primary_key=True)
    timestamp_utc = Column(DateTime, primary_key=True)
    status = Column(Enum(StoreStatusEnum))

    store = relationship('StoreHours', back_populates='statuses')


# create store hours if not found in db trigger
@event.listens_for(StoreStatus, 'before_insert')
def status_before_insert(mapper, connection, target):
    print("before insert")
    session = sessionmaker(bind=connection)()
    store = session.query(StoreHours).filter_by(
        store_id=target.store_id).first()
    if not store:
        store = StoreHours(store_id=target.store_id,
                           timezone_str='America/Chicago')
        session.add(store)
        session.commit()


class StoresHoursSchedule(Base):
    __tablename__ = 'store_hours_schedule'

    id = Column(Integer, primary_key=True)
    store_id = Column(String, ForeignKey(
        'store_hours.store_id'))
    dayOfWeek = Column(Integer)
    start_time_local = Column(Time, nullable=False)
    end_time_local = Column(Time, nullable=False)

    store = relationship('StoreHours', back_populates='schedule')


@event.listens_for(StoresHoursSchedule, 'before_insert')
def schedule_before_insert(mapper, connection, target):
    print("before insert")
    session = sessionmaker(bind=connection)()
    store = session.query(StoreHours).filter_by(
        store_id=target.store_id).first()
    if not store:
        store = StoreHours(store_id=target.store_id,
                           timezone_str='America/Chicago')
        session.add(store)
        session.commit()


class TriggerReport(Base):
    __tablename__ = 'trigger_report'

    report_id = Column(String, primary_key=True)
    status = Column(Enum(TriggerReportStatus))
    progress = Column(Integer, default=0)
