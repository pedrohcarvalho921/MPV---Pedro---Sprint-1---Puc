from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Operacao(Base):
    __tablename__ = 'operacao'

    id = Column("pk_operacao", Integer, primary_key=True)
    ticker_acao = Column(String(), unique=True) # Limite colocado como 5 caracteres, uma vez que toda e qualquer ação tem no máximo 5 dígitos
    quantidade_acao= Column(Integer,nullable=False)
    preco_acao = Column(Float,nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())
    

    comentarios = relationship("Comentario")

    # Definição do relacionamento entre o produto e o comentário dentro da OpenAPI. 

    def __init__(self,ticker_acao:str, quantidade_acao:int , preco_acao:int, data_insercao:Union[DateTime, None] = None):
        
        """
        Cria uma operacao no banco, seguindo os parâmetros abaixo:

        ticker_acao: nome da ação a ser adicionado no banco
        quantidade_acao: insere dentro do banco a quantidade de ações que o usuário possui em carteira.
        preco_acao: No caso, é o preço ou o valor unitário da compra que foi realizada pelo usuário.
        data_insercao: Momento no qual o usuário fez a inclusão dos dados dentro do sistema.

        """
        
        self.ticker_acao=ticker_acao
        self.quantidade_acao = quantidade_acao
        self.preco_acao=preco_acao
        
        if data_insercao:
            self.data_insercao = data_insercao
        



# Ver depois com maior cuidado a função abaixo!
        

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Produto
        """
        self.comentarios.append(comentario)


