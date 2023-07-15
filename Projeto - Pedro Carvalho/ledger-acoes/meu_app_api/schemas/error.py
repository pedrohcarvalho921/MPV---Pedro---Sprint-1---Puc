from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define como a mensagem de erro será representada ao dar erro 404.
    """
    mesage: str
