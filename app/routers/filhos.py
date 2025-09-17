from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.core.security import get_current_secretario
from fastapi import Query

router = APIRouter(prefix="/filhos", tags=["filhos"])

# Endpoint 1: Lista de nomes de filhos com membro_id dos pais
@router.get("/nomes", response_model=List[schemas.filho.FilhoComNomesOut])
def listar_nomes_filhos(db: Session = Depends(database.get_db), user=Depends(get_current_secretario)):
    filhos = db.query(models.filho.Filho).all()
    filhos_out = []
    for filho in filhos:
        mae_nome = None
        pai_nome = None
        if filho.mae:
            mae = db.query(models.membro.Membro).filter_by(id=filho.mae).first()
            if mae:
                mae_nome = mae.nome
        if filho.pai:
            pai = db.query(models.membro.Membro).filter_by(id=filho.pai).first()
            if pai:
                pai_nome = pai.nome
        filho_dict = {
            "id": filho.id,
            "nome": filho.nome,
            "data_nascimento": filho.data_nascimento,
            "batizado": filho.batizado,
            "membro_id": filho.membro_id,
            "mae": mae_nome,
            "pai": pai_nome
        }
        filhos_out.append(filho_dict)
    return filhos_out

# Endpoint 2: Lista de pais (membro_id), retornando pai e mae pelo membro_id


@router.get("/pais", response_model=List[dict])
def listar_pais(
    sexo: str = Query(..., description="M para pais, F para mães"),
    db: Session = Depends(database.get_db), user=Depends(get_current_secretario)
):
    membros = db.query(models.membro.Membro).filter(models.membro.Membro.sexo == sexo).all()
    resultado = []
    for membro in membros:
        if sexo == "M" or sexo == "m":
            filhos = db.query(models.filho.Filho).filter(models.filho.Filho.pai == membro.id).all()
        elif sexo == "F" or sexo == "f":
            filhos = db.query(models.filho.Filho).filter(models.filho.Filho.mae == membro.id).all()
        else:
            filhos = []
        if filhos:
            resultado.append({
                "membro_id": membro.id,
                "nome_membro": membro.nome,
                "filhos": [
                    {
                        "id": filho.id,
                        "nome": filho.nome,
                        "data_nascimento": filho.data_nascimento,
                        "batizado": filho.batizado
                    } for filho in filhos
                ]
            })
    return resultado


# Endpoint para registrar (criar) um filho
@router.post("/", response_model=schemas.filho.FilhoOut)
def criar_filho(filho: schemas.filho.FilhoCreate, db: Session = Depends(database.get_db), user=Depends(get_current_secretario)):
    db_filho = models.filho.Filho(**filho.dict())
    db.add(db_filho)
    db.commit()
    db.refresh(db_filho)
    return db_filho
