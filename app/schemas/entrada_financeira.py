from pydantic import BaseModel
from typing import Optional
from datetime import date

class EntradaFinanceiraBase(BaseModel):
    tipo: str
    valor: float
    data: date
    descricao: Optional[str]
    membro_id: Optional[int]

class EntradaFinanceiraCreate(EntradaFinanceiraBase):
    pass

class EntradaFinanceiraOut(EntradaFinanceiraBase):
    id: int
    class Config:
        orm_mode = True
