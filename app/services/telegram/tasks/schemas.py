import enum
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict


class WorkStatusChoice(enum.Enum):
    IN_PROCESSING = "in_processing"
    IN_WAITING = "in_waiting"
    FAILED = "failed"
    SUCCESS = "success"


class OperationChoice(enum.Enum):
    PARSING = "parsing"
    MAILING = "mailing"


class GetTasksResponse(BaseModel):
    id: int
    created_at: datetime
    job_start: datetime | None
    job_finish: datetime | None
    time_work: time
    title: str
    operation: OperationChoice
    work_status: WorkStatusChoice
    data_count: int
    favorite: bool
    settings: dict

    model_config = ConfigDict(from_attributes=True)
