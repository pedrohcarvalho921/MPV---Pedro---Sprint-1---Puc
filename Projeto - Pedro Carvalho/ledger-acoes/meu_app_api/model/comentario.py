from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id_comentario = Column(Integer, primary_key=True)
    tipo_acao = Column(String(50))
    data_insercao = Column(DateTime,default=datetime.now())
    # Esse código foi criado com o objetivo de associar o ticket da ação incluída dentro do bando de dados a um tipo específico de ações.

    # As ideia inicial seria os inputs nessa classe ficassem restritas aos seguintes valores: Dividendos ; Crescimento ; Crescidendos ; Turnaround

    #Aqui se está linkando a classe Tipo_Acao à classe Operacao, com vinculação à "primary key" da outra tabela!

    operacao = Column(Integer, ForeignKey("operacao.pk_operacao"), nullable=False)

    def __init__(self, tipo_acao:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.tipo_acao = tipo_acao
        if data_insercao:
            self.data_insercao = data_insercao
