from app.schemas.lancamentos import ExcelParser
from app.schemas.dashboard import DashboardResponse, SerieDiaria, SerieAcumulado
from collections import defaultdict

def calcular_dashboard(lancamentos: list[ExcelParser]) -> DashboardResponse:
    total_receitas = sum(l.valor for l in lancamentos if l.tipo == "receita")
    total_despesas = sum(l.valor for l in lancamentos if l.tipo == "despesa")
    lucro_acumulado = total_receitas - total_despesas
    margem_lucro = round((lucro_acumulado / total_receitas) * 100, 2) if total_receitas > 0 else 0.0

    agrupado = defaultdict(lambda: {"receita": 0.0, "despesa": 0.0})
    for l in lancamentos:
        dia = l.data.strftime("%d-%m-%Y")
        if l.tipo == "receita":
            agrupado[dia]["receita"] += l.valor
        else:
            agrupado[dia]["despesa"] += l.valor

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
        lucro_acumulado=round(lucro_acumulado, 2),
        margem_lucro=margem_lucro,
        serie_diaria=serie_diaria,
        serie_acumulado=serie_acumulado,
    )