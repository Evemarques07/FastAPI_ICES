from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_inicio: datetime
    data_final: datetime
    ativo: Optional[bool] = True

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    data_inicio: Optional[datetime]
    data_final: Optional[datetime]
    ativo: Optional[bool]

class EventoOut(EventoBase):
    id: int
    class Config:
        orm_mode = True
