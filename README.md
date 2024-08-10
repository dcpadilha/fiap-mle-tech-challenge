# API EMBRAPA - Vitivinicultura

Esse projeto contém uma API que entrega os dados fornecidos em http://vitibrasil.cnpuv.embrapa.br/

## Recursos
- **FastAPI**: Framework de alta performance utilizado para construção da API.
- **Airflow**: Plataforma de gerenciamento da pipeline de engenharia de dados.
- **MySQL**: Banco de dados utilizado no projeto para armazenar os dados coletados no Scraping.

## Primeiros passos
Para começar nesse projeto, siga as instruções abaixo:

### Pré-requisitos
Esse projeto utiliza o docker compose para orquestração dos containers do projeto. Para você verificar se tem o compose instalado pode rodar o comando:
```bash
docker-compose --version
```

## Instalação
Clone o repositório com:
```bash
git clone git@github.com:dcpadilha/fiap-mle-tech-challenge.git
cd api-vitivinicultura
```

#### Iniciar a aplicação: 
Para iniciar o server em modo de desenvolvimento, utilize:
```bash
`source scrapping/scripts/setup_airflow.sh`
```

Acesse o Airflow em: https://127.0.0.1:8080/home e inicializar as DAGs
Após as DAGs rodarem, as consultas já podem ser feitas na API com o swagger em: https://127.0.0.1/docs

#### No primeiro acesso será necessário criar o usuário admin:
Em um ambiente produtivo, este passo deveria ser feito diretamente no banco.
Para fins instrutivos, criamos um endpoint na API que simplifica esse passo.

Execute o endpoint abaixo com o seguinte Request Body:

```
{
  "usuario": "admin",
  "senha": "admin",
  "role": "ADMIN"
}
```

![](img/endpoint-user.png)

## Documentação:
- Swagger: https://localhost:8000/docs
- Documentação no padrão [Redoc](https://github.com/Redocly/redoc): https://localhost:8000/redoc

## Diagrama da infraestrutura:
![](img/fiap-mle-tech-challenge-v2.drawio.png)

## License