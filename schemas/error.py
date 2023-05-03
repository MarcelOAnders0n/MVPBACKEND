from pydantic import BaseModel

class ErrorSchema(BaseModel):
    '''Define como um erro vai ser apresentado
    '''
    msg: str