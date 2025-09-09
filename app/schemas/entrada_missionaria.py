from pydantic import BaseModel
from typing import Optional
from datetime import date

class EntradaMissionariaCreate(BaseModel):
    tipo: str
    valor: float
    data: date
    descricao: Optional[str] = None
    membro_id: Optional[int] = None

class EntradaMissionariaOut(EntradaMissionariaCreate):
    id: int

    class Config:
        from_attributes = True
