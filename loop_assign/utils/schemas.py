from pydantic import BaseModel


class TriggerResponse(BaseModel):
    report_id: str
