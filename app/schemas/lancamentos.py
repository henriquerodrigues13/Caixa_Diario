from datetime import date
from pydantic import BaseModel, Field, field_serializer, field_validator
from enum import Enum

class TipoLancamento(str, Enum):
    receita = "receita"
    despesa = "despesa"

class ExcelParser(BaseModel):
    data: date
    descricao: str
    tipo: TipoLancamento
    valor: float = Field(gt=0)

    @field_validator("data", mode="before")
    @classmethod
    def parse_data(cls, v):
        if isinstance(v, str):
            from datetime import datetime
            for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
        return v