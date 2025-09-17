from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, database
from app.schemas.escala import EscalaOutComMembro
from app.schemas import escala  
from app.core.security import get_current_diacono
from app.models.escala import Escala

router = APIRouter(prefix="/escalas", tags=["escalas"])

@router.post("/", response_model=escala.EscalaOut)
def create_escala(escala_in: escala.EscalaCreate, db: Session = Depends(database.get_db), user=Depends(get_current_diacono)):
    db_escala = models.escala.Escala(**escala_in.dict())
    db.add(db_escala)
    db.commit()
    db.refresh(db_escala)
    return db_escala

@router.get("/", response_model=List[escala.EscalaOutComMembro])
def list_escalas(skip: int = 0, limit: int = 20, db: Session = Depends(database.get_db), user=Depends(get_current_diacono)):
    escalas = db.query(Escala).join(Escala.membro).offset(skip).limit(limit).all()
    result = []
    for escala_obj in escalas:
        result.append(
            EscalaOutComMembro(
                id=escala_obj.id,
                membro_id=escala_obj.membro_id,
                tipo=escala_obj.tipo,
                data_escala=escala_obj.data_escala,
                ativo=escala_obj.ativo,
                nome_membro=escala_obj.membro.nome if escala_obj.membro else None
            )
        )
    return result

@router.get("/{escala_id}", response_model=escala.EscalaOut)
def get_escala(escala_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_diacono)):
    escala_obj = db.query(models.escala.Escala).filter_by(id=escala_id).first()
    if not escala_obj:
        raise HTTPException(status_code=404, detail="Escala não encontrada")
    return escala_obj

@router.patch("/{escala_id}", response_model=escala.EscalaOut)
def update_escala(escala_id: int, escala_in: escala.EscalaUpdate, db: Session = Depends(database.get_db), user=Depends(get_current_diacono)):
    db_escala = db.query(models.escala.Escala).filter_by(id=escala_id).first()
    if not db_escala:
        raise HTTPException(status_code=404, detail="Escala não encontrada")
    escala_dict = escala_in.dict(exclude_unset=True)
    for key, value in escala_dict.items():
        setattr(db_escala, key, value)
    db.commit()
    db.refresh(db_escala)
    return db_escala

@router.delete("/{escala_id}")
def delete_escala(escala_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_diacono)):
    db_escala = db.query(models.escala.Escala).filter_by(id=escala_id).first()
    if not db_escala:
        raise HTTPException(status_code=404, detail="Escala não encontrada")
    db.delete(db_escala)
    db.commit()
    return {"detail": "Escala removida com sucesso"}
