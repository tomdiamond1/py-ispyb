from pydantic import BaseModel


class EnergyScan(BaseModel):
    energyScanId: int | None

    class Config:
        orm_mode = True
