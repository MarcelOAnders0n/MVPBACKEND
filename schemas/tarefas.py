from pydantic import BaseModel
from model import *

class TarefasSchema(BaseModel):
    tarefa: str 
    status:str

class TarefasDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

class TarefasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura da busca por uma tarefa
    """
    id: str

def apresenta_tarefa(tarefa: Tarefas):
    return { 
        "id": tarefa.id,
        "tarefa": tarefa.tarefa,
        "status": tarefa.status
    }