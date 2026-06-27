from fastapi import APIRouter
from app.schemas.lancamentos import ExcelParser
from app.services.excel_write import json_to_xlsx
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["converte de json pra xlsx"])

@router.post("/export")
async def export(dados: ExcelParser):
    dados_serializados = [dados.model_dump(mode="json")]
    result = await json_to_xlsx(dados_serializados)
    return StreamingResponse(
        result,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=caixa_diario.xlsx"}
    )

