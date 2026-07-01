import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


LANCAMENTO_VALIDO_1 = {
    "data": "27-06-2025",
    "descricao": "Venda de produto",
    "tipo": "receita",
    "valor": 2100.00,
}

LANCAMENTO_VALIDO_2 = {
    "data": "28-06-2025",
    "descricao": "Aluguel do espaço",
    "tipo": "despesa",
    "valor": 1400.00,
}


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ---------- Cenários felizes ----------

@pytest.mark.asyncio
async def test_export_um_lancamento_valido(client):
    response = await client.post("/export", json=[LANCAMENTO_VALIDO_1])

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "attachment; filename=caixa_diario.xlsx" in response.headers["content-disposition"]


@pytest.mark.asyncio
async def test_export_varios_lancamentos_validos(client):
    response = await client.post(
        "/export", json=[LANCAMENTO_VALIDO_1, LANCAMENTO_VALIDO_2]
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ---------- Cenários de erro ----------

@pytest.mark.asyncio
async def test_export_lista_vazia(client):
    response = await client.post("/export", json=[])

    assert response.status_code in (400, 422)


@pytest.mark.asyncio
async def test_export_json_unico_nao_em_lista(client):
    response = await client.post("/export", json=LANCAMENTO_VALIDO_1)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_export_data_formato_invalido(client):
    lancamento_invalido = {**LANCAMENTO_VALIDO_1, "data": "2025/06/27"}
    response = await client.post("/export", json=[lancamento_invalido])

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_export_tipo_invalido(client):
    lancamento_invalido = {**LANCAMENTO_VALIDO_1, "tipo": "transferencia"}
    response = await client.post("/export", json=[lancamento_invalido])

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_export_valor_nao_float(client):
    lancamento_invalido = {**LANCAMENTO_VALIDO_1, "valor": "duzentos"}
    response = await client.post("/export", json=[lancamento_invalido])

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_export_campo_nao_aceito(client):
    lancamento_invalido = {**LANCAMENTO_VALIDO_1, "categoria": "Vendas"}
    response = await client.post("/export", json=[lancamento_invalido])

    assert response.status_code in (200, 422)


@pytest.mark.asyncio
async def test_export_lista_mista_validos_e_invalidos(client):
    lancamento_invalido = {**LANCAMENTO_VALIDO_1, "tipo": "transferencia"}
    response = await client.post(
        "/export", json=[LANCAMENTO_VALIDO_1, lancamento_invalido]
    )

    assert response.status_code == 422