from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, database
from app.core.security import get_current_user

router = APIRouter()

@router.get("/filtrar", response_model=List[dict])
def filtrar_entradas_saidas_gerais(
    descricao: Optional[str] = Query(None),
    membro_id: Optional[int] = Query(None),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
    tipo_movimento: Optional[str] = Query(None, description="entrada, saida ou ambos"),
    tipo_caixa: Optional[str] = Query(None, description="financeiro, missionario, projetos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    resultados = []

    # Função para aplicar filtros comuns
    def aplica_filtros(query, modelo):
        if descricao:
            query = query.filter(modelo.descricao.ilike(f"%{descricao}%"))
        if data_inicio:
            query = query.filter(modelo.data >= data_inicio)
        if data_fim:
            query = query.filter(modelo.data <= data_fim)
        return query

    # Entradas
    if tipo_movimento in [None, "entrada", "ambos"]:
        def add_nome_membro(entrada_dict, membro_id):
            if membro_id:
                membro = db.query(models.membro.Membro).filter_by(id=membro_id).first()
                entrada_dict['nome_membro'] = membro.nome if membro else None
            return entrada_dict

        if tipo_caixa in [None, "financeiro", "ambos"]:
            query = db.query(models.entrada_financeira.EntradaFinanceira)
            query = aplica_filtros(query, models.entrada_financeira.EntradaFinanceira)
            if membro_id:
                query = query.filter(models.entrada_financeira.EntradaFinanceira.membro_id == membro_id)
            query = query.order_by(models.entrada_financeira.EntradaFinanceira.data.desc()).offset(skip).limit(limit)
            for entrada in query.all():
                entrada_dict = entrada.__dict__.copy()
                entrada_dict.pop('_sa_instance_state', None)
                entrada_dict['caixa'] = 'financeiro'
                entrada_dict['movimento'] = 'entrada'
                entrada_dict = add_nome_membro(entrada_dict, entrada_dict.get('membro_id'))
                resultados.append(entrada_dict)
        if tipo_caixa in [None, "missionario", "ambos"]:
            query = db.query(models.entrada_missionaria.EntradaMissionaria)
            query = aplica_filtros(query, models.entrada_missionaria.EntradaMissionaria)
            if membro_id:
                query = query.filter(models.entrada_missionaria.EntradaMissionaria.membro_id == membro_id)
            query = query.order_by(models.entrada_missionaria.EntradaMissionaria.data.desc()).offset(skip).limit(limit)
            for entrada in query.all():
                entrada_dict = entrada.__dict__.copy()
                entrada_dict.pop('_sa_instance_state', None)
                entrada_dict['caixa'] = 'missionario'
                entrada_dict['movimento'] = 'entrada'
                entrada_dict = add_nome_membro(entrada_dict, entrada_dict.get('membro_id'))
                resultados.append(entrada_dict)
        if tipo_caixa in [None, "projetos", "ambos"]:
            query = db.query(models.entrada_projetos.EntradaProjetos)
            query = aplica_filtros(query, models.entrada_projetos.EntradaProjetos)
            if membro_id:
                query = query.filter(models.entrada_projetos.EntradaProjetos.membro_id == membro_id)
            query = query.order_by(models.entrada_projetos.EntradaProjetos.data.desc()).offset(skip).limit(limit)
            for entrada in query.all():
                entrada_dict = entrada.__dict__.copy()
                entrada_dict.pop('_sa_instance_state', None)
                entrada_dict['caixa'] = 'projetos'
                entrada_dict['movimento'] = 'entrada'
                entrada_dict = add_nome_membro(entrada_dict, entrada_dict.get('membro_id'))
                resultados.append(entrada_dict)

    # Saídas (não filtra por membro_id)
    if tipo_movimento in [None, "saida", "ambos"] and not membro_id:
        if tipo_caixa in [None, "financeiro", "ambos"]:
            query = db.query(models.saida_financeira.SaidaFinanceira)
            query = aplica_filtros(query, models.saida_financeira.SaidaFinanceira)
            query = query.order_by(models.saida_financeira.SaidaFinanceira.data.desc()).offset(skip).limit(limit)
            for saida in query.all():
                saida_dict = saida.__dict__.copy()
                saida_dict.pop('_sa_instance_state', None)
                saida_dict['caixa'] = 'financeiro'
                saida_dict['movimento'] = 'saida'
                resultados.append(saida_dict)
        if tipo_caixa in [None, "missionario", "ambos"]:
            query = db.query(models.saida_missionaria.SaidaMissionaria)
            query = aplica_filtros(query, models.saida_missionaria.SaidaMissionaria)
            query = query.order_by(models.saida_missionaria.SaidaMissionaria.data.desc()).offset(skip).limit(limit)
            for saida in query.all():
                saida_dict = saida.__dict__.copy()
                saida_dict.pop('_sa_instance_state', None)
                saida_dict['caixa'] = 'missionario'
                saida_dict['movimento'] = 'saida'
                resultados.append(saida_dict)
        if tipo_caixa in [None, "projetos", "ambos"]:
            query = db.query(models.saida_projetos.SaidaProjetos)
            query = aplica_filtros(query, models.saida_projetos.SaidaProjetos)
            query = query.order_by(models.saida_projetos.SaidaProjetos.data.desc()).offset(skip).limit(limit)
            for saida in query.all():
                saida_dict = saida.__dict__.copy()
                saida_dict.pop('_sa_instance_state', None)
                saida_dict['caixa'] = 'projetos'
                saida_dict['movimento'] = 'saida'
                resultados.append(saida_dict)

    return resultados or []