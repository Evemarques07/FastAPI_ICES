from pydantic import BaseModel, constr
from typing import Optional

class UsuarioBase(BaseModel):
    cpf: constr(min_length=11, max_length=14)
    ativo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    senha: str
    membro_id: int

class UsuarioOut(UsuarioBase):
    id: int
    membro_id: int
    nome: Optional[str] = None
    class Config:
        from_attributes = True
