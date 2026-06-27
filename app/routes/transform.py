from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import excel_parser
from app.schemas import lancamentos


router = APIRouter(tags=["Trasformação de xlsx para json"])

@router.post("/transform")
async def transform(file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")
    result = await excel_parser.parser(file)
    for row in result:
        try:
            lancamentos.ExcelParser(**row)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"O arquivo não tem a estrutura aceita pela ferramenta ")

    return result
