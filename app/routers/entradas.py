from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from app.schemas.entrada_missionaria import EntradaMissionariaCreate
from app.schemas.entrada_projetos import EntradaProjetosCreate

from app import models, schemas, database
from app.core.security import get_current_user, get_current_financeiro

router = APIRouter(prefix="/entradas", tags=["entradas"])

@router.post("/", response_model=schemas.entrada_financeira.EntradaFinanceiraOut)
def create_entrada(entrada: schemas.entrada_financeira.EntradaFinanceiraCreate, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = models.entrada_financeira.EntradaFinanceira(**entrada.dict())
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

@router.get("/filtradas", response_model=List[dict])
def list_entradas_filtradas(
    tipo: str = None,
    descricao: str = None,
    nome_membro: str = None,
    data_inicio: str = None,
    data_fim: str = None,
    user=Depends(get_current_financeiro),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(
        models.entrada_financeira.EntradaFinanceira,
        models.membro.Membro.nome
    ).join(models.membro.Membro, models.entrada_financeira.EntradaFinanceira.membro_id == models.membro.Membro.id, isouter=True)
    # Filtros flexíveis (LIKE para tipo, descricao, nome do membro)
    if tipo:
        query = query.filter(models.entrada_financeira.EntradaFinanceira.tipo.ilike(f"%{tipo}%"))
    if descricao:
        query = query.filter(models.entrada_financeira.EntradaFinanceira.descricao.ilike(f"%{descricao}%"))
    if nome_membro:
        query = query.filter(models.membro.Membro.nome.ilike(f"%{nome_membro}%"))
    if data_inicio:
        query = query.filter(models.entrada_financeira.EntradaFinanceira.data >= data_inicio)
    if data_fim:
        query = query.filter(models.entrada_financeira.EntradaFinanceira.data <= data_fim)

    query = query.order_by(models.entrada_financeira.EntradaFinanceira.data.desc())

    result = []
    for entrada, nome_membro in query.offset(skip).limit(limit):
        entrada_dict = entrada.__dict__.copy()
        entrada_dict.pop('_sa_instance_state', None)
        entrada_dict['nome_membro'] = nome_membro
        result.append(entrada_dict)
    return result

@router.get("/", response_model=List[dict])
def list_entradas(
    user=Depends(get_current_financeiro),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(
        models.entrada_financeira.EntradaFinanceira,
        models.membro.Membro.nome
    ).join(models.membro.Membro, models.entrada_financeira.EntradaFinanceira.membro_id == models.membro.Membro.id, isouter=True) \
     .order_by(models.entrada_financeira.EntradaFinanceira.data.desc()) \
     .offset(skip).limit(limit)

    result = []
    for entrada, nome_membro in query:
        entrada_dict = entrada.__dict__.copy()
        entrada_dict.pop('_sa_instance_state', None)
        entrada_dict['nome_membro'] = nome_membro
        result.append(entrada_dict)
    return result

@router.get("/{entrada_id}", response_model=schemas.entrada_financeira.EntradaFinanceiraOut)
def get_entrada(entrada_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    entrada = db.query(models.entrada_financeira.EntradaFinanceira).filter(models.entrada_financeira.EntradaFinanceira.id == entrada_id).first()
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    return entrada

# buscar entrada missionária por id

@router.get("/missoes/{entrada_id}", response_model=schemas.entrada_missionaria.EntradaMissionariaOut)
def get_entrada_missionaria(entrada_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    entrada = db.query(models.entrada_missionaria.EntradaMissionaria).filter(models.entrada_missionaria.EntradaMissionaria.id == entrada_id).first()
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    return entrada

# buscar entrada de projetos por id

@router.get("/projetos/{entrada_id}", response_model=schemas.entrada_projetos.EntradaProjetosOut)
def get_entrada_projetos(entrada_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    entrada = db.query(models.entrada_projetos.EntradaProjetos).filter(models.entrada_projetos.EntradaProjetos.id == entrada_id).first()
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    return entrada

@router.post("/missoes", response_model=dict)
def create_entrada_missionaria(
    entrada: EntradaMissionariaCreate,
    db: Session = Depends(database.get_db),
    user=Depends(get_current_financeiro)
):
    db_entrada = models.entrada_missionaria.EntradaMissionaria(**entrada.dict())
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    entrada_dict = db_entrada.__dict__.copy()
    entrada_dict.pop('_sa_instance_state', None)
    return entrada_dict

# criar entrada de projetos
@router.post("/projetos", response_model=dict)
def create_entrada_projetos(
    entrada: EntradaProjetosCreate,
    db: Session = Depends(database.get_db),
    user=Depends(get_current_financeiro)
):
    db_entrada = models.entrada_projetos.EntradaProjetos(**entrada.dict())
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    entrada_dict = db_entrada.__dict__.copy()
    entrada_dict.pop('_sa_instance_state', None)
    return entrada_dict


# Atualizar entrada financeira
@router.put("/financeiro/{entrada_id}", response_model=schemas.entrada_financeira.EntradaFinanceiraOut)
def update_entrada_financeira(entrada_id: int, entrada: schemas.entrada_financeira.EntradaFinanceiraCreate, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = db.query(models.entrada_financeira.EntradaFinanceira).filter_by(id=entrada_id).first()
    if not db_entrada:
        raise HTTPException(status_code=404, detail="Entrada financeira não encontrada")
    for key, value in entrada.dict().items():
        setattr(db_entrada, key, value)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

# Atualizar entrada missionária
@router.put("/missoes/{entrada_id}", response_model=dict)
def update_entrada_missionaria(entrada_id: int, entrada: dict, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = db.query(models.entrada_missionaria.EntradaMissionaria).filter_by(id=entrada_id).first()
    if not db_entrada:
        raise HTTPException(status_code=404, detail="Entrada missionária não encontrada")
    for key, value in entrada.items():
        setattr(db_entrada, key, value)
    db.commit()
    db.refresh(db_entrada)
    entrada_dict = db_entrada.__dict__.copy()
    entrada_dict.pop('_sa_instance_state', None)
    return entrada_dict

# Atualizar entrada de projetos
@router.put("/projetos/{entrada_id}", response_model=dict)
def update_entrada_projetos(entrada_id: int, entrada: dict, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = db.query(models.entrada_projetos.EntradaProjetos).filter_by(id=entrada_id).first()
    if not db_entrada:
        raise HTTPException(status_code=404, detail="Entrada de projetos não encontrada")
    for key, value in entrada.items():
        setattr(db_entrada, key, value)
    db.commit()
    db.refresh(db_entrada)
    entrada_dict = db_entrada.__dict__.copy()
    entrada_dict.pop('_sa_instance_state', None)
    return entrada_dict

# Deletar entrada financeira
@router.delete("/financeiro/{entrada_id}", response_model=dict)
def delete_entrada_financeira(entrada_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = db.query(models.entrada_financeira.EntradaFinanceira).filter_by(id=entrada_id).first()
    if not db_entrada:
        raise HTTPException(status_code=404, detail="Entrada financeira não encontrada")
    db.delete(db_entrada)
    db.commit()
    return {"message": "Entrada financeira deletada com sucesso"}

# Deletar entrada missionária
@router.delete("/missoes/{entrada_id}", response_model=dict)
def delete_entrada_missionaria(entrada_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = db.query(models.entrada_missionaria.EntradaMissionaria).filter_by(id=entrada_id).first()
    if not db_entrada:
        raise HTTPException(status_code=404, detail="Entrada missionária não encontrada")
    db.delete(db_entrada)
    db.commit()
    return {"message": "Entrada missionária deletada com sucesso"}

# Deletar entrada de projetos
@router.delete("/projetos/{entrada_id}", response_model=dict)
def delete_entrada_projetos(entrada_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_financeiro)):
    db_entrada = db.query(models.entrada_projetos.EntradaProjetos).filter_by(id=entrada_id).first()
    if not db_entrada:
        raise HTTPException(status_code=404, detail="Entrada de projetos não encontrada")
    db.delete(db_entrada)
    db.commit()
    return {"message": "Entrada de projetos deletada com sucesso"}


@router.get("/membro/{membro_id}", response_model=dict)
def list_entradas_por_membro(membro_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    # Entradas financeiras
    entradas = db.query(models.entrada_financeira.EntradaFinanceira) \
        .filter(models.entrada_financeira.EntradaFinanceira.membro_id == membro_id) \
        .order_by(models.entrada_financeira.EntradaFinanceira.data.desc()) \
        .all()
    # Entradas missionárias
    entradas_missionarias = db.query(models.entrada_missionaria.EntradaMissionaria) \
        .filter(models.entrada_missionaria.EntradaMissionaria.membro_id == membro_id) \
        .order_by(models.entrada_missionaria.EntradaMissionaria.data.desc()) \
        .all()
    # Entradas projetos
    entradas_projetos = db.query(models.entrada_projetos.EntradaProjetos) \
        .filter(models.entrada_projetos.EntradaProjetos.membro_id == membro_id) \
        .order_by(models.entrada_projetos.EntradaProjetos.data.desc()) \
        .all()

    agrupadas = {}
    for entrada in entradas:
        tipo = f"financeira_{entrada.tipo or 'Outro'}"
        if tipo not in agrupadas:
            agrupadas[tipo] = []
        agrupadas[tipo].append(schemas.entrada_financeira.EntradaFinanceiraOut.model_validate(entrada, from_attributes=True))
    for entrada in entradas_missionarias:
        tipo = f"missionaria_{entrada.tipo or 'Outro'}"
        if tipo not in agrupadas:
            agrupadas[tipo] = []
        entrada_dict = entrada.__dict__.copy()
        entrada_dict.pop('_sa_instance_state', None)
        agrupadas[tipo].append(entrada_dict)
    for entrada in entradas_projetos:
        tipo = f"projetos_{entrada.tipo or 'Outro'}"
        if tipo not in agrupadas:
            agrupadas[tipo] = []
        entrada_dict = entrada.__dict__.copy()
        entrada_dict.pop('_sa_instance_state', None)
        agrupadas[tipo].append(entrada_dict)
    return agrupadas

@router.get("/listar/missoes", response_model=List[dict])
def list_entradas_missoes(
    user=Depends(get_current_financeiro),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(
        models.entrada_missionaria.EntradaMissionaria,
        models.membro.Membro.nome
    ).join(models.membro.Membro, models.entrada_missionaria.EntradaMissionaria.membro_id == models.membro.Membro.id, isouter=True) \
     .order_by(models.entrada_missionaria.EntradaMissionaria.data.desc()) \
     .offset(skip).limit(limit)

    result = []
    for entrada, nome_membro in query:
        entrada_dict = entrada.__dict__.copy()
        entrada_dict.pop('_sa_instance_state', None)
        entrada_dict['nome_membro'] = nome_membro
        result.append(entrada_dict)
    return result

@router.get("/listar/projetos", response_model=List[dict])
def list_entradas_projetos(
    user=Depends(get_current_financeiro),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(
        models.entrada_projetos.EntradaProjetos,
        models.membro.Membro.nome
    ).join(models.membro.Membro, models.entrada_projetos.EntradaProjetos.membro_id == models.membro.Membro.id, isouter=True) \
     .order_by(models.entrada_projetos.EntradaProjetos.data.desc()) \
     .offset(skip).limit(limit)

    result = []
    for entrada, nome_membro in query:
        entrada_dict = entrada.__dict__.copy()
        entrada_dict.pop('_sa_instance_state', None)
        entrada_dict['nome_membro'] = nome_membro
        result.append(entrada_dict)
    return result

@router.get("/soma", response_model=dict)
def soma_entradas(
    tipo: str = None,  # 'financeira', 'missionaria', 'projetos' ou None para todas
    data_inicio: str = None,
    data_fim: str = None,
    user=Depends(get_current_financeiro),
    db: Session = Depends(database.get_db)
):
    filtros = []
    if data_inicio:
        filtros.append(lambda col: col.data >= data_inicio)
    if data_fim:
        filtros.append(lambda col: col.data <= data_fim)

    def soma_model(model):
        query = db.query(func.sum(model.valor))
        for f in filtros:
            query = query.filter(f(model))
        return query.scalar() or 0

    resultado = {}
    if not tipo or tipo == 'financeira':
        resultado['soma_financeiras'] = soma_model(models.entrada_financeira.EntradaFinanceira)
    if not tipo or tipo == 'missionaria':
        resultado['soma_missoes'] = soma_model(models.entrada_missionaria.EntradaMissionaria)
    if not tipo or tipo == 'projetos':
        resultado['soma_projetos'] = soma_model(models.entrada_projetos.EntradaProjetos)
    return resultado