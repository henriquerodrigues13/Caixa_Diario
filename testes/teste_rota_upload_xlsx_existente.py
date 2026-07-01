from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

ARQUIVOS_DIR = Path(__file__).parent / "arquivos_teste_xlsx"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def _abrir_xlsx(nome: str):
    caminho = ARQUIVOS_DIR / nome
    return caminho.open("rb")


# ---------- Cenários felizes ----------

@pytest.mark.asyncio
async def test_upload_xlsx_um_registro_valido(client):
    with _abrir_xlsx("teste1.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste1.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    registro = data[0]
    assert set(registro.keys()) == {"data", "descricao", "tipo", "valor"}
    assert len(registro["data"]) == 10
    assert registro["data"][2] == "-" and registro["data"][5] == "-"
    assert registro["tipo"] in ("receita", "despesa")
    assert isinstance(registro["valor"], (int, float))


@pytest.mark.asyncio
async def test_upload_xlsx_varios_registros_validos(client):
    with _abrir_xlsx("teste2.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste2.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 1

    for registro in data:
        assert set(registro.keys()) == {"data", "descricao", "tipo", "valor"}
        assert registro["data"][2] == "-" and registro["data"][5] == "-"
        assert registro["tipo"] in ("receita", "despesa")


# ---------- Cenários de erro ----------

@pytest.mark.asyncio
async def test_upload_xlsx_vazio(client):
    with _abrir_xlsx("teste3.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste3.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_xlsx_data_formato_invalido(client):
    with _abrir_xlsx("teste4.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste4.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_xlsx_tipo_invalido(client):
    with _abrir_xlsx("teste5.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste5.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_xlsx_colunas_extras(client):
    with _abrir_xlsx("teste6.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste6.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code in (200, 400)
    if response.status_code == 200:
        data = response.json()
        for registro in data:
            assert "categoria" not in registro


@pytest.mark.asyncio
async def test_upload_xlsx_valor_nao_float(client):
    with _abrir_xlsx("teste7.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste7.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_mais_de_um_arquivo(client):
    with _abrir_xlsx("teste1.xlsx") as f1, _abrir_xlsx("teste2.xlsx") as f2:
        response = await client.post(
            "/upload/xlsx_existente",
            files=[
                (
                    "file",
                    (
                        "teste1.xlsx",
                        f1,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                ),
                (
                    "file",
                    (
                        "teste2.xlsx",
                        f2,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                ),
            ],
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4


@pytest.mark.asyncio
async def test_upload_xlsx_registros_validos_e_invalidos(client):
    with _abrir_xlsx("teste8.xlsx") as f:
        response = await client.post(
            "/upload/xlsx_existente",
            files={
                "file": (
                    "teste8.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 400