from fastapi import APIRouter, HTTPException
from app.schemas.lancamentos import ExcelParser
from app.services.excel_write import json_to_xlsx
from fastapi.responses import StreamingResponse
from typing import List

router = APIRouter(tags=["converte de json pra xlsx"])

@router.post("/export")
async def export(dados: List[ExcelParser]):
    if not dados:
        raise HTTPException(status_code=400, detail="A lista de lançamentos não pode estar vazia")
    dados_serializados = [item.model_dump(mode="json") for item in dados]
    result = await json_to_xlsx(dados_serializados)
    return StreamingResponse(
        result,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=caixa_diario.xlsx"}
    )

