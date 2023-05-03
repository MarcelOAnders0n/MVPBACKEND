from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from flask_cors import CORS
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from schemas import *

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefas_tag = Tag(name="Tarefas", description="Rotas relacionadas a tabela de tarefas")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')



@app.get('/tarefas', tags=[tarefas_tag])
def getTarefas():
    session = Session()
    tarefas = session.query(Tarefas).all()
    return jsonify({'tarefas': [apresenta_tarefa(tarefa) for tarefa in tarefas]})

@app.post('/tarefas', tags=[tarefas_tag], responses={
    "400": ErrorSchema
})
def postTarefas(form: TarefasSchema):
    tarefa = Tarefas(
        tarefa=form.tarefa,
        status=form.status
    )
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(tarefa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_tarefa(tarefa), 201

    except IntegrityError as e:
        session.rollback()
        err = e.args
        return {"mesage": err}, 400
    
@app.delete('/tarefas', tags=[tarefas_tag],
            responses={"200": TarefasDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefasBuscaSchema):
    """Deleta uma Tarefa a partir do id de terefa informado
    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_id = unquote(unquote(query.id))
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Tarefas).filter(Tarefas.id == tarefa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Tarefa removida", "id": tarefa_id}
    else:
        # se a tarefa não foi encontrada
        error_msg = "Tarefa não encontrada na base :/"
        return {"mesage": error_msg}, 404

@app.put('/tarefas', tags=[tarefas_tag],
            responses={"200": TarefasDelSchema, "404": ErrorSchema})
def att_tarefa(query: TarefasBuscaSchema):
    """Atualiza uma Tarefa a partir do id de Tarefa informado
    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_id = unquote(unquote(query.id))
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    print(tarefa_id)
    count = session.query(Tarefas).filter(Tarefas.id == tarefa_id).first()
    print(count)
    if count.status == '':
        count.status = "checked"
    else:
        count.status = ''
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Tarefa atualizada", "id": tarefa_id}
    else:
        # se o Tarefa não foi encontrada
        error_msg = "Tarefa não encontrada na base :/"
        return {"mesage": error_msg}, 404