from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, database
from app.schemas import evento
from app.core.security import get_current_user

router = APIRouter(prefix="/eventos", tags=["eventos"])

# Buscar eventos pelo título usando LIKE
@router.get("/buscar", response_model=List[evento.EventoOut])
def buscar_eventos_por_titulo(
    termo: str = Query(..., description="Título do evento"),
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    termo_like = f"%{termo}%"
    eventos = db.query(models.evento.Evento).filter(models.evento.Evento.titulo.ilike(termo_like)).all()
    return eventos

@router.post("/", response_model=evento.EventoOut)
def create_evento(evento: evento.EventoCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_evento = models.evento.Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@router.get("/", response_model=List[evento.EventoOut])
def list_eventos(skip: int = 0, limit: int = 20, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    eventos = db.query(models.evento.Evento).offset(skip).limit(limit).all()
    return eventos

# listar eventos ativos sem paginação
@router.get("/ativos", response_model=List[evento.EventoOut])
def list_eventos_ativos(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    eventos = db.query(models.evento.Evento).filter_by(ativo=True).all()
    return eventos

@router.get("/{evento_id}", response_model=evento.EventoOut)
def get_evento(evento_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    evento = db.query(models.evento.Evento).filter_by(id=evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return evento

@router.patch("/{evento_id}", response_model=evento.EventoOut)
def update_evento(evento_id: int, evento: evento.EventoUpdate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_evento = db.query(models.evento.Evento).filter_by(id=evento_id).first()
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    evento_dict = evento.dict(exclude_unset=True)
    for key, value in evento_dict.items():
        setattr(db_evento, key, value)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@router.delete("/{evento_id}")
def delete_evento(evento_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_evento = db.query(models.evento.Evento).filter_by(id=evento_id).first()
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    db.delete(db_evento)
    db.commit()
    return {"detail": "Evento removido com sucesso"}
