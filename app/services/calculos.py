from app.schemas.lancamentos import ExcelParser
from app.schemas.dashboard import DashboardResponse, SerieDiaria, SerieAcumulado
from collections import defaultdict

def calcular_dashboard(lancamentos: list[ExcelParser]) -> DashboardResponse:
    total_receitas = sum(l.valor for l in lancamentos if l.tipo == "receita")
    total_despesas = sum(l.valor for l in lancamentos if l.tipo == "despesa")
    lucro_acumulado = total_receitas - total_despesas
    caixa = round((total_receitas - total_despesas), 2) if total_receitas > 0 else 0.0

    agrupado = defaultdict(lambda: {"receita": 0.0, "despesa": 0.0})

    for l in lancamentos:
        dia = l.data.strftime("%d-%m-%Y")
        if l.tipo == "receita":
            agrupado[dia]["receita"] += l.valor
        else:
            agrupado[dia]["despesa"] += l.valor

    dias_unicos = len(agrupado)

    media_receita = round(total_receitas / dias_unicos, 2) if dias_unicos > 0 else 0.0
    media_despesa = round(total_despesas / dias_unicos, 2) if dias_unicos > 0 else 0.0
    media_lucro = round(lucro_acumulado / dias_unicos, 2) if dias_unicos > 0 else 0.0

    serie_diaria = [
        SerieDiaria(data=dia, receita=v["receita"], despesa=v["despesa"])
        for dia, v in sorted(agrupado.items())
    ]

    saldo = 0.0
    serie_acumulado = []
    for item in serie_diaria:
        saldo += item.receita - item.despesa
        serie_acumulado.append(SerieAcumulado(data=item.data, saldo=round(saldo, 2)))

    return DashboardResponse(
        total_receitas=round(total_receitas, 2),
        total_despesas=round(total_despesas, 2),
        media_receita=media_receita,
        media_despesa=media_despesa,
        media_lucro=media_lucro,
        caixa=caixa,
        serie_diaria=serie_diaria,
        serie_acumulado=serie_acumulado,
    )