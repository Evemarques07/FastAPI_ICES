from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import date

class MembroBase(BaseModel):
    nome: str
    data_nascimento: date
    telefone: Optional[str]
    email: Optional[EmailStr]
    endereco: Optional[str]
    data_entrada: date
    ativo: Optional[bool] = True
    cpf: Optional[constr(min_length=11, max_length=14)]
    foto: Optional[str] = None  # Agora é uma URL
    tipo: Optional[str] = 'membro'


class MembroCreate(MembroBase):
    senha: Optional[str]

class MembroUpdate(BaseModel):
    nome: Optional[str]
    data_nascimento: Optional[date]
    telefone: Optional[str]
    email: Optional[EmailStr]
    endereco: Optional[str]
    data_entrada: Optional[date]
    ativo: Optional[bool]
    cpf: Optional[constr(min_length=11, max_length=14)]
    tipo: Optional[str]

class MembroOut(MembroBase):
    id: int
    class Config:
        orm_mode = True
