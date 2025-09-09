from pydantic import BaseModel
from typing import Optional
from datetime import date

class SaidaFinanceiraBase(BaseModel):
    tipo: str
    valor: float
    data: date
    descricao: Optional[str]

class SaidaFinanceiraCreate(SaidaFinanceiraBase):
    pass

class SaidaFinanceiraOut(SaidaFinanceiraBase):
    id: int
    class Config:
        orm_mode = True
