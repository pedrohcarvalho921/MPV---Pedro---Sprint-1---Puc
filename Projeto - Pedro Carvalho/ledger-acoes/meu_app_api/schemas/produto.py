from pydantic import BaseModel
from typing import Optional, List
from model.produto import Operacao

from schemas import ComentarioSchema


class OperacaoSchema(BaseModel):
    """ Define como será inserida uma nova operação de ações a ser inserido deve ser representado
    """
    ticker_acao: str = 'KLBN3' 
    quantidade_acao: int=100
    preco_acao: float=3.65


class OperacaoBuscaSchema(BaseModel):
    """ Definição da estrutura para pesquisa dentro do banco de dados da operação, que será feita com base no id no banco de dados.
    """
    ticker_acao: str
    
class OperacaoBuscaSchema2(BaseModel):
    """ Definição da estrutura para pesquisa dentro do banco de dados da operação, que será feita com base no id no banco de dados.
    """
    id: int

   
class ListagemOperacoesSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[OperacaoSchema]


def apresenta_produtos(produtos: List[Operacao]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "ticker_acao": produto.ticker_acao,
            "quantidade": produto.quantidade_acao,
            "preco_acao": produto.preco_acao,
        })

    return {"operacoes": result}


class OperacaoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto e o seu tipo.
    """
    id: int=1
    ticker_acao: str = "KLBN3"
    quantidade: Optional[int] = 100
    preco_acao: float = 3.65
    total_cometarios: int = 1
    #tipo_acao = str = "Dividendos"
    comentarios:List[ComentarioSchema]


class OperacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    ticker_acao: str
    

def apresenta_produto(produto: Operacao):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "ticker_acao": produto.ticker_acao,
        "quantidade": produto.quantidade_acao,
        "preco": produto.preco_acao,
        "total_cometarios": len(produto.comentarios),
        "comentarios": [{"texto": comentario} for comentario in produto.comentarios]
    }
