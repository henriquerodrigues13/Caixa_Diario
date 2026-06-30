# caixa-diario-backend

API REST para leitura e geração de planilhas de caixa diário financeiro. Stateless — não possui banco de dados.

---

## Rotas

### `POST /upload/dashboard`

Recebe um arquivo `.xlsx` com lançamentos financeiros, valida a estrutura e retorna os dados calculados para o dashboard.

**Request**

- Content-Type: `multipart/form-data`
- Campo: `file` — arquivo `.xlsx`

O arquivo deve conter exatamente as seguintes colunas:

| Coluna | Tipo | Observação |
|---|---|---|
| `data` | string | Formato aceito: `DD-MM-YYYY`  |
| `descricao` | string | Texto livre |
| `tipo` | string | Apenas `"receita"` ou `"despesa"` |
| `valor` | float | Número positivo |

**Response** `200 OK`

```json
{
  "total_receitas": 18400.00,
  "total_despesas": 12750.00,
  "lucro_acumulado": 5650.00,
  "margem_lucro": 30.7,
  "serie_diaria": [
    { "data": "01-06-2025", "receita": 2100.00, "despesa": 1400.00 }
  ],
  "serie_acumulado": [
    { "data": "01-06-2025", "saldo": 700.00 }
  ]
}
```

**Erros**

| Código | Motivo |
|---|---|
| `400` | Arquivo não é `.xlsx` |
| `400` | Estrutura de colunas inválida |

---

### `POST /export`

Recebe um lançamento em JSON e retorna um arquivo `.xlsx` pronto para download. Se quiser exportar múltiplos lançamentos, o frontend deve enviar um por um ou adaptar o endpoint para receber uma lista.

**Request**

- Content-Type: `application/json`

```json
{
  "data": "27-06-2025",
  "descricao": "Venda de produto",
  "tipo": "receita",
  "valor": 2100.00
}
```

| Campo | Tipo | Observação |
|---|---|---|
| `data` | string | Formatos aceitos: `DD/MM/YYYY`, `DD-MM-YYYY` ou `YYYY-MM-DD` |
| `descricao` | string | Texto livre |
| `tipo` | string | Apenas `"receita"` ou `"despesa"` |
| `valor` | float | Número positivo |

**Response** `200 OK`

- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Header: `Content-Disposition: attachment; filename=caixa_diario.xlsx`
- Body: arquivo `.xlsx` binário

---

## Como rodar localmente

### Pré-requisitos

- Python 3.11 ou superior
- Git

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/henriquerodrigues13/caixa-diario-backend.git
cd caixa-diario-backend
```

**2. Crie e ative o ambiente virtual**

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -e ".[dev]"
```

**4. Rode o FastAPI**

```bash
fastapi dev ./app/main.py
```

O servidor estará disponível em `http://localhost:8000`.

A documentação interativa estará em `http://localhost:8000/docs`.

---

## Estrutura do projeto

```
caixa-diario-backend/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   └── export.py
│   ├── schemas/
│   │   ├── lancamentos.py
│   │   └── dashboard.py
│   └── services/
│       ├── excel_parser.py
│       ├── excel_write.py
│       └── calculos.py
├── pyproject.toml
├── .env.example
└── README.md
```
