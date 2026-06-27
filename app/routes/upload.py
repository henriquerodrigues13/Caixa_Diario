from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import excel_parser
from app.schemas import lancamentos
from app.schemas.lancamentos import ExcelParser
from typing import List
from app.services.calculos import calcular_dashboard
from app.schemas.dashboard import DashboardResponse


router = APIRouter(tags=["converte de xlsx para json"])

@router.post("/upload/xlsx_existente", response_model=List[ExcelParser] )
async def upload_xls_to_json(file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")
    result = await excel_parser.parser(file)
    try:
        dados_validados = [lancamentos.ExcelParser(**row) for row in result]
        return [l.model_dump() for l in dados_validados]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"O arquivo não tem a estrutura aceita pela ferramenta: {str(e)}")

@router.post("/upload/dashboard", response_model=DashboardResponse)
async def upload_dashboard(file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")
    result = await excel_parser.parser(file)
    try:
        dados_validados = [lancamentos.ExcelParser(**row) for row in result]
        return calcular_dashboard(dados_validados)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"O arquivo não tem a estrutura aceita pela ferramenta: {str(e)}")

