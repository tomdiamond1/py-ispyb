from pydantic import BaseModel


class XFEFluorescenceSpectrum(BaseModel):
    xfeFluorescenceSpectrumId: int | None

    class Config:
        orm_mode = True
