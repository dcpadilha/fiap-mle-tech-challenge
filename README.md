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

#### Após a aplicação iniciada, será necessário criar a tabela no MySQL (enquanto não foi feita a migration):
Para acessar o container do MySQL, primeiro verifica o nome do container através de:
```bash
docker ps
```

Após isso, copie o nome do container do MySQL e rode o comando abaixo:
```bash
docker exec -it {nome_do_container} bash
```

Com isso você estará dentro do container. Acesse o MySQL com:
```bash
mysql -u root -p
```
A senha é "root"

Rode o comando `show database;` e após isso `use tech_challenge`

Com isso a tabela pode ser criada através da DDL:
```SQL
CREATE TABLE vitibrasil (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    ano VARCHAR(4) ,
    origem VARCHAR(100) ,
    sub_origem VARCHAR(100) ,
    categoria VARCHAR(100) ,
    sub_categoria VARCHAR(100) ,
    valor DECIMAL(18, 2) ,
    qtde_kg INT ,
    inserted_at DATETIME ,
    last_updated DATETIME DEFAULT (NOW()),
    PRIMARY KEY (id)
);
```

Após a tabela criada você pode acessar o Airflow em: https://127.0.0.1:8080/home e inicializar as DAGs
Após as DAGs rodarem, as consultas já podem ser feitas na API com o swagger em: https://127.0.0.1/docs

## Documentação:
- Swagger: https://localhost:8000/docs
- Documentação no padrão [Redoc](https://github.com/Redocly/redoc): https://localhost:8000/redoc

## Diagrama da infraestrutura:
![](img/fiap-mle-tech-challenge-v2.drawio.png)

## License