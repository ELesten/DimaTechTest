from pydantic import BaseModel


class ExceptionSchema(BaseModel):
    status_code: int
    er_message: str
    er_details: str
