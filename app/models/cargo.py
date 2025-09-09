from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cargo(Base):
    __tablename__ = 'cargos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    membros = relationship('CargoMembro', back_populates='cargo')

class CargoMembro(Base):
    __tablename__ = 'cargos_membros'
    id = Column(Integer, primary_key=True, index=True)
    membro_id = Column(Integer, ForeignKey('membros.id'), nullable=False)
    cargo_id = Column(Integer, ForeignKey('cargos.id'), nullable=False)
    cargo = relationship('Cargo', back_populates='membros')
    membro = relationship('Membro', back_populates='cargos')
