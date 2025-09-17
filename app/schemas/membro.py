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
    sexo: Optional[str] = None
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    estado_civil: Optional[str] = None
    data_casamento: Optional[date] = None
    nome_conjuge: Optional[str] = None
    data_nascimento_conjuge: Optional[date] = None
    data_batismo: Optional[date] = None


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
    sexo: Optional[str] = None
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    estado_civil: Optional[str] = None
    data_casamento: Optional[date] = None
    nome_conjuge: Optional[str] = None
    data_nascimento_conjuge: Optional[date] = None
    data_batismo: Optional[date] = None

class MembroOut(MembroBase):
    id: int
    class Config:
        from_attributes = True


class MembrosListOut(BaseModel):
    total: int
    membros: List[MembroOut]
