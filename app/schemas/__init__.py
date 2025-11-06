from pydantic import BaseModel


class HeathCheckResponse(BaseModel):
    status: str
