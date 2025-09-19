from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatrimonioBase(BaseModel):
    nome_item: str
    tipo: str
    preco_aquisicao: float
    data_aquisicao: date
    observacoes: Optional[str] = None

class PatrimonioCreate(PatrimonioBase):
    pass

class PatrimonioUpdate(BaseModel):
    nome_item: Optional[str] = None
    tipo: Optional[str] = None
    preco_aquisicao: Optional[float] = None
    data_aquisicao: Optional[date] = None
    observacoes: Optional[str] = None

class PatrimonioOut(PatrimonioBase):
    id: int
    class Config:
        from_attributes = True
