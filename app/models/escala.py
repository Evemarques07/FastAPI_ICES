from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Escala(Base):
    __tablename__ = "escalas"

    id = Column(Integer, primary_key=True, index=True)
    membro_id = Column(Integer, ForeignKey("membros.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    data_escala = Column(DateTime, nullable=False)
    ativo = Column(Boolean, default=True)
    membro = relationship("Membro", back_populates="escalas")
