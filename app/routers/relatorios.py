from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import models, database
from app.core.security import get_current_user
from datetime import datetime

router = APIRouter(prefix="/relatorios", tags=["relatorios"])

@router.get("/financeiro")
def relatorio_financeiro(
    mes: int = Query(..., ge=1, le=12),
    ano: int = Query(..., ge=1900),
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    from sqlalchemy import extract
    from sqlalchemy import func
    # Entradas e saídas do mês/ano solicitado
    entradas = db.query(models.entrada_financeira.EntradaFinanceira).filter(
        extract('month', models.entrada_financeira.EntradaFinanceira.data) == mes,
        extract('year', models.entrada_financeira.EntradaFinanceira.data) == ano
    ).all()
    saidas = db.query(models.saida_financeira.SaidaFinanceira).filter(
        extract('month', models.saida_financeira.SaidaFinanceira.data) == mes,
        extract('year', models.saida_financeira.SaidaFinanceira.data) == ano
    ).all()
    entradas_missoes = db.query(models.entrada_missionaria.EntradaMissionaria).filter(
        extract('month', models.entrada_missionaria.EntradaMissionaria.data) == mes,
        extract('year', models.entrada_missionaria.EntradaMissionaria.data) == ano
    ).all()
    saidas_missoes = db.query(models.saida_missionaria.SaidaMissionaria).filter(
        extract('month', models.saida_missionaria.SaidaMissionaria.data) == mes,
        extract('year', models.saida_missionaria.SaidaMissionaria.data) == ano
    ).all()
    entradas_projetos = db.query(models.entrada_projetos.EntradaProjetos).filter(
        extract('month', models.entrada_projetos.EntradaProjetos.data) == mes,
        extract('year', models.entrada_projetos.EntradaProjetos.data) == ano
    ).all()
    saidas_projetos = db.query(models.saida_projetos.SaidaProjetos).filter(
        extract('month', models.saida_projetos.SaidaProjetos.data) == mes,
        extract('year', models.saida_projetos.SaidaProjetos.data) == ano
    ).all()

    # Saldo anterior: entradas - saídas até mês anterior
    def saldo_anterior(entrada_model, saida_model):
        soma_entradas = db.query(func.sum(entrada_model.valor)).filter(
            extract('year', entrada_model.data) < ano
        ).scalar() or 0
        soma_entradas += db.query(func.sum(entrada_model.valor)).filter(
            extract('year', entrada_model.data) == ano,
            extract('month', entrada_model.data) < mes
        ).scalar() or 0
        soma_saidas = db.query(func.sum(saida_model.valor)).filter(
            extract('year', saida_model.data) < ano
        ).scalar() or 0
        soma_saidas += db.query(func.sum(saida_model.valor)).filter(
            extract('year', saida_model.data) == ano,
            extract('month', saida_model.data) < mes
        ).scalar() or 0
        return soma_entradas - soma_saidas

    saldo_anterior_financeiro = saldo_anterior(models.entrada_financeira.EntradaFinanceira, models.saida_financeira.SaidaFinanceira)
    saldo_anterior_missoes = saldo_anterior(models.entrada_missionaria.EntradaMissionaria, models.saida_missionaria.SaidaMissionaria)
    saldo_anterior_projetos = saldo_anterior(models.entrada_projetos.EntradaProjetos, models.saida_projetos.SaidaProjetos)
    total_entradas = sum(e.valor for e in entradas)
    total_saidas = sum(s.valor for s in saidas)
    total_entradas_missoes = sum(e.valor for e in entradas_missoes)
    total_saidas_missoes = sum(s.valor for s in saidas_missoes)
    total_entradas_projetos = sum(e.valor for e in entradas_projetos)
    total_saidas_projetos = sum(s.valor for s in saidas_projetos)
    def serialize_item(item):
        membro_nome = None
        if hasattr(item, 'membro_id') and item.membro_id:
            membro = db.query(models.membro.Membro).filter_by(id=item.membro_id).first()
            if membro:
                membro_nome = membro.nome
        d = item.__dict__.copy()
        d['membro_nome'] = membro_nome
        return d

    entradas_serializadas = [serialize_item(e) for e in entradas]
    saidas_serializadas = [serialize_item(s) for s in saidas]
    entradas_missoes_serializadas = [serialize_item(e) for e in entradas_missoes]
    saidas_missoes_serializadas = [serialize_item(s) for s in saidas_missoes]
    entradas_projetos_serializadas = [serialize_item(e) for e in entradas_projetos]
    saidas_projetos_serializadas = [serialize_item(s) for s in saidas_projetos]

    def fmt(valor):
        return round(float(valor), 2) if valor is not None else 0.0

    return {
        "mes": mes,
        "ano": ano,
        "saldo_anterior_financeiro": fmt(saldo_anterior_financeiro),
        "saldo_atual_financeiro": fmt(saldo_anterior_financeiro + total_entradas - total_saidas),
        "saldo_anterior_missoes": fmt(saldo_anterior_missoes),
        "saldo_atual_missoes": fmt(saldo_anterior_missoes + total_entradas_missoes - total_saidas_missoes),
        "saldo_anterior_projetos": fmt(saldo_anterior_projetos),
        "saldo_atual_projetos": fmt(saldo_anterior_projetos + total_entradas_projetos - total_saidas_projetos),
        "total_entradas": fmt(total_entradas),
        "total_saidas": fmt(total_saidas),
        "entradas": entradas_serializadas,
        "saidas": saidas_serializadas,
        "total_entradas_missoes": fmt(total_entradas_missoes),
        "total_saidas_missoes": fmt(total_saidas_missoes),
        "entradas_missoes": entradas_missoes_serializadas,
        "saidas_missoes": saidas_missoes_serializadas,
        "total_entradas_projetos": fmt(total_entradas_projetos),
        "total_saidas_projetos": fmt(total_saidas_projetos),
        "entradas_projetos": entradas_projetos_serializadas,
        "saidas_projetos": saidas_projetos_serializadas
    }

@router.get("/financeiro_resumido")
def relatorio_financeiro_resumido(
    mes: int = Query(..., ge=1, le=12),
    ano: int = Query(..., ge=1900),
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    from sqlalchemy import extract, func
    entradas = db.query(models.entrada_financeira.EntradaFinanceira).filter(
        extract('month', models.entrada_financeira.EntradaFinanceira.data) == mes,
        extract('year', models.entrada_financeira.EntradaFinanceira.data) == ano
    ).all()
    saidas = db.query(models.saida_financeira.SaidaFinanceira).filter(
        extract('month', models.saida_financeira.SaidaFinanceira.data) == mes,
        extract('year', models.saida_financeira.SaidaFinanceira.data) == ano
    ).all()
    entradas_missoes = db.query(models.entrada_missionaria.EntradaMissionaria).filter(
        extract('month', models.entrada_missionaria.EntradaMissionaria.data) == mes,
        extract('year', models.entrada_missionaria.EntradaMissionaria.data) == ano
    ).all()
    saidas_missoes = db.query(models.saida_missionaria.SaidaMissionaria).filter(
        extract('month', models.saida_missionaria.SaidaMissionaria.data) == mes,
        extract('year', models.saida_missionaria.SaidaMissionaria.data) == ano
    ).all()
    entradas_projetos = db.query(models.entrada_projetos.EntradaProjetos).filter(
        extract('month', models.entrada_projetos.EntradaProjetos.data) == mes,
        extract('year', models.entrada_projetos.EntradaProjetos.data) == ano
    ).all()
    saidas_projetos = db.query(models.saida_projetos.SaidaProjetos).filter(
        extract('month', models.saida_projetos.SaidaProjetos.data) == mes,
        extract('year', models.saida_projetos.SaidaProjetos.data) == ano
    ).all()

    def saldo_anterior(entrada_model, saida_model):
        soma_entradas = db.query(func.sum(entrada_model.valor)).filter(
            extract('year', entrada_model.data) < ano
        ).scalar() or 0
        soma_entradas += db.query(func.sum(entrada_model.valor)).filter(
            extract('year', entrada_model.data) == ano,
            extract('month', entrada_model.data) < mes
        ).scalar() or 0
        soma_saidas = db.query(func.sum(saida_model.valor)).filter(
            extract('year', saida_model.data) < ano
        ).scalar() or 0
        soma_saidas += db.query(func.sum(saida_model.valor)).filter(
            extract('year', saida_model.data) == ano,
            extract('month', saida_model.data) < mes
        ).scalar() or 0
        return soma_entradas - soma_saidas

    saldo_anterior_financeiro = saldo_anterior(models.entrada_financeira.EntradaFinanceira, models.saida_financeira.SaidaFinanceira)
    saldo_anterior_missoes = saldo_anterior(models.entrada_missionaria.EntradaMissionaria, models.saida_missionaria.SaidaMissionaria)
    saldo_anterior_projetos = saldo_anterior(models.entrada_projetos.EntradaProjetos, models.saida_projetos.SaidaProjetos)

    # Agrupamento por tipo
    def agrupa_por_tipo(lista, campo_tipo="tipo"):
        agrupado = {}
        for item in lista:
            tipo = getattr(item, campo_tipo, None)
            if tipo:
                agrupado[tipo] = agrupado.get(tipo, 0) + float(item.valor)
        return {k: round(v, 2) for k, v in agrupado.items()}

    total_entradas = sum(e.valor for e in entradas)
    total_saidas = sum(s.valor for s in saidas)
    total_entradas_missoes = sum(e.valor for e in entradas_missoes)
    total_saidas_missoes = sum(s.valor for s in saidas_missoes)
    total_entradas_projetos = sum(e.valor for e in entradas_projetos)
    total_saidas_projetos = sum(s.valor for s in saidas_projetos)

    entradas_por_tipo = agrupa_por_tipo(entradas)
    entradas_missoes_por_tipo = agrupa_por_tipo(entradas_missoes)
    entradas_projetos_por_tipo = agrupa_por_tipo(entradas_projetos)

    def serialize_item(item):
        membro_nome = None
        if hasattr(item, 'membro_id') and item.membro_id:
            membro = db.query(models.membro.Membro).filter_by(id=item.membro_id).first()
            if membro:
                membro_nome = membro.nome
        d = item.__dict__.copy()
        d['membro_nome'] = membro_nome
        return d

    saidas_serializadas = [serialize_item(s) for s in saidas]
    saidas_missoes_serializadas = [serialize_item(s) for s in saidas_missoes]
    saidas_projetos_serializadas = [serialize_item(s) for s in saidas_projetos]

    def fmt(valor):
        return round(float(valor), 2) if valor is not None else 0.0

    return {
        "mes": mes,
        "ano": ano,
        "saldo_anterior_financeiro": fmt(saldo_anterior_financeiro),
        "saldo_atual_financeiro": fmt(saldo_anterior_financeiro + total_entradas - total_saidas),
        "saldo_anterior_missoes": fmt(saldo_anterior_missoes),
        "saldo_atual_missoes": fmt(saldo_anterior_missoes + total_entradas_missoes - total_saidas_missoes),
        "saldo_anterior_projetos": fmt(saldo_anterior_projetos),
        "saldo_atual_projetos": fmt(saldo_anterior_projetos + total_entradas_projetos - total_saidas_projetos),
        "total_entradas": fmt(total_entradas),
        "entradas_por_tipo": entradas_por_tipo,
        "total_saidas": fmt(total_saidas),
        "saidas": saidas_serializadas,
        "total_entradas_missoes": fmt(total_entradas_missoes),
        "entradas_missoes_por_tipo": entradas_missoes_por_tipo,
        "total_saidas_missoes": fmt(total_saidas_missoes),
        "saidas_missoes": saidas_missoes_serializadas,
        "total_entradas_projetos": fmt(total_entradas_projetos),
        "entradas_projetos_por_tipo": entradas_projetos_por_tipo,
        "total_saidas_projetos": fmt(total_saidas_projetos),
        "saidas_projetos": saidas_projetos_serializadas
    }