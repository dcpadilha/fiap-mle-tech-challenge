from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados
# Exemplo: "mysql+pymysql://usuario:senha@localhost/dbname"
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/tech_challenge"

# Cria o engine (motor) de conexão
engine = create_engine(DATABASE_URL)

# Cria uma classe base para definir as tabelas do banco de dados
Base = declarative_base()

# Cria uma fábrica de sessões para gerenciar as conexões com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
