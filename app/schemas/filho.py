from pydantic import BaseModel
from typing import Optional
from datetime import date

class FilhoBase(BaseModel):
    nome: str
    data_nascimento: Optional[date]
    batizado: Optional[bool] = False
    membro_id: Optional[int]
    mae: Optional[int]
    pai: Optional[int]

class FilhoOut(FilhoBase):
    id: int
    class Config:
        from_attributes = True

class FilhoComNomesOut(BaseModel):
    id: int
    nome: str
    data_nascimento: Optional[date]
    batizado: Optional[bool] = False
    membro_id: Optional[int]
    mae: Optional[str] = None
    pai: Optional[str] = None
    class Config:
        from_attributes = True

class FilhoCreate(FilhoBase):
    pass
