from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Filho(Base):
    __tablename__ = 'filhos'
    id = Column(Integer, primary_key=True, index=True)
    membro_id = Column(Integer, ForeignKey('membros.id'), nullable=True)
    mae = Column(Integer, ForeignKey('membros.id'), nullable=True)
    pai = Column(Integer, ForeignKey('membros.id'), nullable=True)
    nome = Column(String(255), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    batizado = Column(Boolean, default=False)

    membro = relationship('Membro', foreign_keys=[membro_id])
    mae_rel = relationship('Membro', foreign_keys=[mae])
    pai_rel = relationship('Membro', foreign_keys=[pai])
