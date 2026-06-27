from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class ExcelParser(BaseModel):
    data: datetime
    descricao: str
    tipo: TipoLancamento
    valor: float = Field(gt=0)

class TipoLancamento(str, Enum):
    receita = "receita"
    despesa = "despesa"
