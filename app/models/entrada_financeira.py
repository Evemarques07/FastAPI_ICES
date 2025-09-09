from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EntradaFinanceira(Base):
    __tablename__ = 'entradas_financeiras'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(255), nullable=True)
    membro_id = Column(Integer, ForeignKey('membros.id'), nullable=True)
    membro = relationship('Membro', back_populates='entradas')
