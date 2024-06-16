# ÍNDICE

1. [SOBRE](#sobre)
2. [CONFIGURANDO O AMBIENTE](#configurando)
    1. Instalando o ambiente virtual
3. [API](#api)
    1. Endpoints
        1. `[GET] /dados/`
    2. Inicializando a API
        1. Em modo de desenvolvimento

# 1 SOBRE <a name="sobre"></a>

\<A fazer\>

# 2 CONFIGURANDO O AMBIENTE <a name="configurando"></a>

## 2.1 Instalando o ambiente virtual

> **PRÉ-REQUISITOS**
> - [conda](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
> - [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

```bash
conda create --prefix ./.venv python=3.12.3
conda activate ./.venv
poetry install
```

# 3 API <a name="api"></a>

## 3.1 Endpoints

### `[GET] /dados/`

> Endpoint para download dos arquivos (.csv) que estão disponíveis no site da Embrapa. 

São 5 arquivos que estão disponibilizados nos seguintes endpoints:

- `/dados/producao/`: Produção de vinhos, sucos e derivados do Rio Grande do Sul;
- `/dados/processamento/`: Quantidade de uvas processadas no Rio Grande do Sul;
- `/dados/comercializacao/`: Comercialização de vinhos e derivados no Rio Grande do Sul;
- `/dados/importacao/`: Importação de derivados de uva;
- `/dados/exportacao/`: Exportação de derivados de uva.

## 3.2 Inicializando a API

### Em modo de desenvolvimento

```bash
fastapi dev main.py
```
