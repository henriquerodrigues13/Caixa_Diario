from pydantic import BaseModel

class SerieDiaria(BaseModel):
    data: str
    receita: float
    despesa: float

class SerieAcumulado(BaseModel):
    data: str
    saldo: float

class DashboardResponse(BaseModel):
    total_receitas: float
    total_despesas: float
    caixa : float
    media_receita: float
    media_despesa: float
    media_lucro: float
    serie_diaria: list[SerieDiaria]
    serie_acumulado: list[SerieAcumulado]
