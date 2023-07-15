from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Operacao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API - Ledger de ações", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição das tags dentro do contexto da OpenAPI
home_tag = Tag(name="Documentação", description="Explicação de documentação das rotas da API")
produto_tag = Tag(name="Operações em Bolsa", description=" Inclusão de operações de ações (ticker, quantidade e preço), vizualização dos resultados no banco e deleção de itens já incluídos. Para fins práticos, Ação e Ticker serão tratados como sinônimos para o nome da ação, enquanto Operação se referirá ao conjunto de valores (Linha inteira de valores dentro do banco de dados)")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário relacionado à uma operação de bolsa de valores já inserida dentro da base de dados.")

@app.get('/', tags=[home_tag])
def home():
    """Faz o redirecionamento da porta local para a mesma porta local com "/openapi", para que se possa ler a documentação da API e suas respectivas rotas.
    """
    return redirect('/openapi')

@app.post('/produto', tags=[produto_tag],
          responses={"200": OperacaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def cadastrar_operacao(form: OperacaoSchema):
    """Adiciona uma nova operação em bolsa de valores à base de dados da aplicação.

    Retorna em JSON (assim como todas as outras rodas da aplicação) uma representação dos valores associados à operação em bolsa de forma análoga ao usuário pelo front-end.
    """
    produto = Operacao(ticker_acao=form.ticker_acao,
                       quantidade_acao=form.quantidade_acao,
                       preco_acao=form.preco_acao)
    
    logger.debug(f"Adicionado o ticker de nome: '{produto.ticker_acao}'")
    try:
        # Cria uma conexão com o banco de dados
        session = Session()
        # Adiciona uma operaçao à base de dados.
        session.add(produto)
        session.commit()
        logger.debug(f"Adicionado o ticker de nome: '{produto.ticker_acao}'")
        return apresenta_produto(produto), 200

    except IntegrityError:
        # Bloqueia o acesso ao banco de dados do novo input pelo usuário, caso já exista aquela operação
        error_msg = "Ação com o mesmo nome já está salvo dentro da base. O dado que você inseriu foi esse mesmo?"
        logger.warning(f"Erro ao adicionar a Ação '{produto.ticker_acao}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception:
        # Caso ocorra algum tipo de erro com a comunicação com o servidor, a mensagem abaixo será incluída dentro dos logs da aplicação.
        error_msg = "Não foi possível salvar o ticker dentro da base."
        logger.warning(f"Erro ao salvar o ticker: '{produto.ticker_acao}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemOperacoesSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos as operações registradas dentro dos dados da aplicação.

    Retorna os valores inseridos no banco até aquele momento.
    """
    logger.debug(f"Processando valores... ")
    session = Session()
    # Abre uma sessão de conexão com o banco de dados da aplicação, fazendo uma query dentro do banco de dados e retornando todos os valores inseridos no banco até aquele momento.
    produtos = session.query(Operacao).all()

    if not produtos:
        # Caso não haja operações de bolsa de valores no banco de dados, o programa irá retornar a lista como vazia e a requisição como válida.
        return {"Ações inseridas dentro da base": []}, 200
    else:
        logger.debug(f"%d operações em bolsa de valores encontradas!" % len(produtos)) # Irá registrar no logger, o número de operações registradas ao se fazer uso desse método em específico.
        # Retorna a representação das operações presentes no banco até aquele momento.
        print(produtos)
        return apresenta_produtos(produtos), 200

@app.get('/produto', tags=[produto_tag],
         responses={"200": OperacaoViewSchema, "404": ErrorSchema})
def get_produto(query: OperacaoBuscaSchema2):
    """Consulta o banco de dados por uma operação realizada pelo usuário a partir do ID da operação (número de inserção dentro do banco de dados)

    Retorna uma representação das operações e comentários associados.
    """
    operacao_id = query.id
    logger.debug(f"Coletando dados sobre a operação #{operacao_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Operacao).filter(Operacao.id == operacao_id).first()

    if not produto:
        # Mensagem de erro caso a ação / operação não for encontrada.
        error_msg = "Ação não encontrada dentro da base de dados. É esse o nome mesmo da ação?"
        logger.warning(f"Erro ao buscar a operação '{operacao_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Operação encontrada: '{produto.ticker_acao}'")
        # Retorna os valores associados àquele ID, sendo o ticker da ação, a quantidade e os valores.
        return apresenta_produto(produto), 200





@app.delete('/produto', tags=[produto_tag],
            responses={"200": OperacaoDelSchema, "404": ErrorSchema})
def del_operacao(query: OperacaoBuscaSchema):
    """Deleta uma operação a partir do ticker da ação comprada dentro do contexto da operação

    Retorna os valores que foram deletados do banco de dados, confirmando a deleção da operação em bolsa de valores do banco de dados da aplicação via requisição 200. Caso não exista, irá dar erro 404.
    """
    operacao_nome = unquote(unquote(query.ticker_acao))
    print(operacao_nome)
    logger.debug(f"Deletando dados sobre a ação #{operacao_nome}")
    # Abre uma sessão de conexão com o banco de dados da aplicação, fazendo uma query dentro do banco de dados e retornando todos os valores inseridos no banco até aquele momento.
    session = Session()
    # Faz a efetiva deleção do item do banco de dados a partir do nome do ticker da ação e de todos os seus valores associados (Preço e Quantidade).
    count = session.query(Operacao).filter(Operacao.ticker_acao == operacao_nome).delete()
    session.commit()

    if count:
        # Gera dentro do logger as informações abaixo, confirmando que a requisição foi feita, com a deleção do item do Banco de dados.
        logger.debug(f"Deletado ticker {operacao_nome}")
        return {"mesage": "Ação removida removido", "Ticker": operacao_nome}
    else:
        # Mensagem de erro abaixo, mencionando que a ação que se tentou apagar já não está presente dentro do banco de dados.
        error_msg = "Ação não encontrada dentro da base de dados. É esse o nome mesmo da ação?"
        logger.warning(f"Erro ao deletar a ação #'{operacao_nome}.', {error_msg}")
        return {"mesage": error_msg}, 404
















