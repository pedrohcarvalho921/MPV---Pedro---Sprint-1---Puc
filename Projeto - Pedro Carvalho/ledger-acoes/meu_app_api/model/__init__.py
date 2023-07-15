from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.comentario import Comentario
from model.produto import Operacao

db_path = "database/"
if not os.path.exists(db_path):
   os.makedirs(db_path)

db_url = 'sqlite:///%s/banco_dados.sqlite3' % db_path
engine = create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url) 
Base.metadata.create_all(engine)

#Cria o diretório do banco de dados e o banco de dados em SQLite3 com as tabelas a partir da definição nos arquivos "Comentario" e "Produto"