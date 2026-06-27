from io import BytesIO

from openpyxl import Workbook

async def json_to_xlsx(dados: list[dict]):
    wb = Workbook()
    ws = wb.active

    headers = list(dados[0].keys())
    ws.append(headers)

    for item in dados:
        ws.append(list(item.values()))

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return buffer


