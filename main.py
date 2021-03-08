from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi  import FastAPI , HTTPException
from pydantic import BaseModel, Field
from typing   import List,Dict, Optional
import uuid

class DisciplinaChangableEntry(BaseModel):
    nome_disciplina  :  Optional[str]       = Field(..., example="Mega Dados")
    nome_professor   :  Optional[str]       = Field(..., example="Fabio Ayres")
    anotacoes        :  Optional[str]       = Field(..., example="Fazer projeto SQL,")

class NotaEntry(BaseModel):
    nome_da_prova : str
    nota   :   int

class DisciplinaEntry(BaseModel):
    nome_disciplina  :  str                 = Field(..., example="Mega Dados")
    nome_professor   :  Optional[str]       = Field(..., example="Fabio Ayres")
    anotacoes        :  Optional[str]       = Field(..., example="Fazer projeto SQL,")
    notas_id         :  Optional[List[str]] = Field(..., example=[])

class AlunoEntry(BaseModel):
    nome_aluno       : str                  = Field(..., example="José")
    disciplinas_id   : Optional[List[str]]  = Field(..., example=[])

app = FastAPI()

db  = {
    "Alunos" : {
        "4abf3d52-7fbd-11eb-baba-d7de924f09cd": {
        "nome_aluno": "José",
        "disciplinas_id": ["a00f52fe-7fbf-11eb-baba-d7de924f09cd","b00f52fe-7fbf-11eb-baba-d7de924f09cd"]
        },
        "7fgf3d52-7fbd-11eb-baba-d7de924f09cd": {
        "nome_aluno": "Hélio",
        "disciplinas_id": []
        },
    },
    "Disciplinas" : {
        "a00f52fe-7fbf-11eb-baba-d7de924f09cd":{
            "nome_disciplina": "Mega Dados",
            "nome_professor": "Fabio Ayres",
            "anotacoes": " Estudar para a prova",
            "notas_id": ["4114e75e-7fc0-11eb-baba-d7de924f09cd"]
        },
        "b00f52fe-7fbf-11eb-baba-d7de924f09cd":{
            "nome_disciplina": "Cloud",
            "nome_professor": "Raul",
            "anotacoes": "Fazer H0",
            "notas_id": ["6714e75e-7fc0-11eb-baba-d7de924f09cd"]
        },
    },
    "Notas" : {
        "4114e75e-7fc0-11eb-baba-d7de924f09cd":{
            "nome_da_prova": "PF",
            "nota": 1000
        },
        "6714e75e-7fc0-11eb-baba-d7de924f09cd":{
            "nome_da_prova": "PI",
            "nota": 1000
        },
    }
}

#---Handler Error ---# OK!
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc):
    return PlainTextResponse(str(exc), status_code=400)

#---Criar Aluno ------# OK!
@app.post("/aluno")
def registre_aluno(aluno: AlunoEntry):
    ID = str(uuid.uuid1())
    db["Alunos"][ID] = aluno.dict()
    return db["Alunos"][ID]

#---Criar Disciplinas ------# OK!
@app.post("/alunos/{id_aluno}/disciplinas")
def registre_disciplina(id_aluno: str, disciplina: DisciplinaEntry):
    if id_aluno in db["Alunos"]:
        ID =str(uuid.uuid1())
        db["Alunos"][id_aluno]["disciplinas_id"].append(ID)
        db["Disciplinas"][ID] = disciplina.dict()
        return db["Disciplinas"][ID]
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Criar Nota ------# OK!
@app.post("/alunos/{id_aluno}/disciplinas/{id_disciplina}/nota")
def registre_nota(id_aluno:str ,id_disciplina: str, nota: NotaEntry):
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            ID =str(uuid.uuid1())
            db["Disciplinas"][id_disciplina]["notas_id"].append(ID)
            db["Notas"][ID] = nota.dict()
            return db["Notas"][ID]
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")

# ---Todos os Alunos---# OK!
@app.get("/alunos/todos")
def todos_alunos():
    return db["Alunos"]

# ---Todas as Disciplinas---# OK!
@app.get("/alunos/{id_aluno}/disciplinas/todas")
def todas_disciplinas(id_aluno:str ):
    if id_aluno in db["Alunos"]:
        return db["Disciplinas"]
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")


# ---Todos os Nomes de Disciplinas ---# OK!
@app.get("/alunos/{id_aluno}/disciplinas/nomes")
def todos_nomes_disciplina(id_aluno: str):
    nome_disciplina=[]
    if id_aluno in db["Alunos"]:
        lista = db["Alunos"][id_aluno]["disciplinas_id"]
        for disciplina_id in lista:
            nome_disciplina.append(db["Disciplinas"][disciplina_id]["nome_disciplina"])
        return nome_disciplina
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Todas as Anotações de uma Matéria Especifica ---#
@app.get("/alunos/{id_aluno}/disciplinas/{id_disciplina}/anotacoes")
def todas_anotacoes_disciplina(id_aluno: str, id_disciplina: str=None):
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            return db["Disciplinas"][id_disciplina]["anotacoes"]
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Todas as Notas de uma Matéria Especifica ---#
@app.get("/alunos/{id_aluno}/disciplinas/{id_disciplina}/notas")
def todas_notas_disciplina(id_aluno: str,id_disciplina: str):
    notas_disciplina=[]
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            lista = db["Disciplinas"][id_disciplina]["notas_id"]
            for notas_id in lista:
                notas_disciplina.append(db["Notas"][notas_id]["nota"])
            return notas_disciplina
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Altera disciplina---#
@app.patch("/alunos/{id_aluno}/disciplinas/{id_disciplina}/nome/disciplina", response_model= DisciplinaChangableEntry)
def altera_nome_disciplina(id_aluno:str ,id_disciplina: str, nome_disciplina: DisciplinaChangableEntry):
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            stored_disciplina = db["Disciplinas"][id_disciplina]
            stored_disciplina_model = DisciplinaEntry(**stored_disciplina)
            update_data = nome_disciplina.dict(exclude_unset=True)
            updated_disciplina = stored_disciplina_model.copy(update=update_data)
            db["Disciplinas"][id_disciplina] = updated_disciplina.dict()
            return updated_disciplina
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
        raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Altera disciplina Nota---#
@app.patch("/alunos/{id_aluno}/disciplinas/{id_disciplina}/notas/{id_nota}", response_model= NotaEntry)
def altera_nota_disciplina(id_aluno:str ,id_disciplina: str,id_nota:str ,nome_nota: NotaEntry):
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            if id_nota in db["Disciplinas"][id_disciplina]["notas_id"]:
                stored_nota = db["Notas"][id_nota]
                stored_nota_model = NotaEntry(**stored_nota)
                update_data = nome_nota.dict(exclude_unset=True)
                updated_disciplina = stored_nota_model.copy(update=update_data)
                db["Notas"][id_nota] = updated_disciplina.dict()
                return updated_disciplina
            else:
                raise HTTPException(status_code=404, detail="nota não encontrada")
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
            raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Deletar Nota ---#
@app.delete("/alunos/{id_aluno}/disciplinas/{id_disciplina}/notas/{id_nota}/deleta")
def delete_nota(id_aluno:str ,id_disciplina: str, id_nota: str):
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            if id_nota in db["Disciplinas"][id_disciplina]["notas_id"]:
                db["Disciplinas"][id_disciplina]["notas_id"].remove(id_nota)
                del db["Notas"][id_nota]
            else:
                raise HTTPException(status_code=404, detail="nota não encontrada")
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
            raise HTTPException(status_code=404, detail="aluno não encontrado")

#---Deletar disciplina ---#
@app.delete("/alunos/{id_aluno}/disciplina/{id_disciplina}")
def delete_disciplina(id_aluno:str ,id_disciplina: str):
    if id_aluno in db["Alunos"]:
        if id_disciplina in db["Alunos"][id_aluno]["disciplinas_id"]:
            db["Alunos"][id_aluno]["disciplinas_id"].remove(id_disciplina)
            del db["Disciplinas"][id_disciplina]
        else:
            raise HTTPException(status_code=404, detail="disciplina não encontrada")
    else:
            raise HTTPException(status_code=404, detail="aluno não encontrado")


