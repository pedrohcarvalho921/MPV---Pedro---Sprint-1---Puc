from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    id_comentario: int = 1
    #tipo_acao: str = "Favor colocar: Dividendos, Crescimento, Crescidendos ou Turnaround!"
