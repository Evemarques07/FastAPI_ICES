from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EscalaBase(BaseModel):
    membro_id: int
    tipo: str
    data_escala: datetime
    ativo: Optional[bool] = True

class EscalaOut(EscalaBase):
    id: int
    class Config:
        orm_mode = True

class EscalaOutComMembro(EscalaOut):
    nome_membro: Optional[str]

class EscalaCreate(EscalaBase):
    pass

class EscalaUpdate(BaseModel):
    membro_id: Optional[int]
    tipo: Optional[str]
    data_escala: Optional[datetime]
    ativo: Optional[bool]


