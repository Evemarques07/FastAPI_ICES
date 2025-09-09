from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.core.security import get_current_user, get_password_hash

router = APIRouter(prefix="/membros", tags=["membros"])

@router.post("/", response_model=schemas.membro.MembroOut)
def create_membro(membro: schemas.membro.MembroCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_membro = models.membro.Membro(**membro.dict(exclude={"senha", "foto"}))
    if membro.foto:
        db_membro.foto = membro.foto
    db.add(db_membro)
    db.commit()
    db.refresh(db_membro)
    if membro.senha and membro.cpf:
        senha_hash = get_password_hash(membro.senha)
        db_usuario = models.usuario.Usuario(cpf=membro.cpf, senha_hash=senha_hash, membro_id=db_membro.id)
        db.add(db_usuario)
        db.commit()
    return db_membro

# Filtrar membros por nome ou cpf
from fastapi import Query

@router.get("/filtrar", response_model=List[schemas.membro.MembroOut])
def filtrar_membros(
    termo: str = Query(..., description="Nome ou CPF para busca"),
    db: Session = Depends(database.get_db), user=Depends(get_current_user)
):
    query = db.query(models.membro.Membro).filter(models.membro.Membro.id != 1)
    termo_like = f"%{termo}%"
    membros = query.filter(
        (models.membro.Membro.nome.ilike(termo_like)) |
        (models.membro.Membro.cpf.ilike(termo_like))
    ).all()
    return membros

@router.get("/", response_model=List[schemas.membro.MembroOut])
def list_membros(
    skip: int = Query(0, ge=0, description="Itens a pular"),
    limit: int = Query(20, ge=1, le=50, description="Quantidade máxima de itens"),
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    membros = db.query(models.membro.Membro).filter(models.membro.Membro.id != 1).offset(skip).limit(limit).all()
    return membros


@router.patch("/{membro_id}/ativar", response_model=schemas.membro.MembroOut)
def ativar_membro(membro_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    membro = db.query(models.membro.Membro).filter_by(id=membro_id).first()
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    membro.ativo = not membro.ativo
    db.commit()
    db.refresh(membro)
    return membro

# Atualizar membro
@router.patch("/{membro_id}", response_model=schemas.membro.MembroOut)
def update_membro(membro_id: int, membro: schemas.membro.MembroCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_membro = db.query(models.membro.Membro).filter_by(id=membro_id).first()
    if not db_membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    for key, value in membro.dict(exclude_unset=True, exclude={"senha", "foto"}).items():
        setattr(db_membro, key, value)
    if membro.foto:
        db_membro.foto = membro.foto
    db.commit()
    db.refresh(db_membro)
    return db_membro

