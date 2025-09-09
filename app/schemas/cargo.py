from pydantic import BaseModel
from typing import Optional

class CargoBase(BaseModel):
    nome: str

class CargoCreate(CargoBase):
    pass

class CargoOut(CargoBase):
    id: int
    class Config:
        from_attributes = True
