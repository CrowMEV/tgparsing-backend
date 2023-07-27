import enum


class WorkStatusChoice(enum.Enum):
    IN_PROCESSING = "in_processing"
    IN_WAITING = "in_waiting"
    FAILED = "failed"
    SUCCESS = "success"


class OperationChoice(enum.Enum):
    PARSING = "parsing"
    MAILING = "mailing"
