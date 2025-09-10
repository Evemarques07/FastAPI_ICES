from pydantic import BaseModel
from datetime import date
from typing import Optional

class EventoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_inicio: date
    data_final: date
    ativo: Optional[bool] = True

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    data_inicio: Optional[date]
    data_final: Optional[date]
    ativo: Optional[bool]

class EventoOut(EventoBase):
    id: int
    class Config:
        orm_mode = True
