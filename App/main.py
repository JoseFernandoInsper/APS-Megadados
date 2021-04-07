from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi  import Depends ,FastAPI , HTTPException
from sqlalchemy.orm import Session
import crud as crud
import schemas as schemas
import models as models
import database as dt
from typing import List

import uuid

dt.Base.metadata.create_all(bind=dt.engine)

app = FastAPI()

# Dependency
def get_db():
    db = dt.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

app = FastAPI()

#---Handler Error ---# OK!
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc):
    return PlainTextResponse(str(exc), status_code=400)

#---Criar Aluno ------# OK!
@app.post("/aluno/", response_model=schemas.Aluno)
def registre_aluno(aluno: schemas.AlunoCreate ,db:Session = Depends(get_db)):
    return crud.register_aluno(db=db, aluno=aluno)

#---Criar Disciplina ------# OK!
@app.post("/alunos/{aluno_id}/disciplinas/", response_model=schemas.Disciplina)
def registre_disciplina(db:Session,aluno_id: int, disciplina: schemas.DisciplinaCreate):
    db_aluno = crud.get_alunos(db, aluno_id=aluno_id)
    if db_aluno:
        return crud.register_disciplina(db=db, aluno=aluno_id, disciplina=disciplina)
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

#---Criar Nota ------# OK!
@app.post("/alunos/{aluno_id}/disciplinas/{disciplina_id}/nota")
def registre_nota(db:Session,aluno_id:int ,disciplina_id: int, nota: schemas.Nota):
    db_aluno = crud.get_alunos(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno:
        if db_disciplina:
            return crud.register_nota(db=db, aluno=aluno_id ,disciplina=disciplina_id ,nota=nota)
        else:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

# ---Todos os Alunos---# OK!
@app.get("/alunos/", response_model=List[schemas.Aluno])
def todos_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_alunos(db, skip=skip, limit=limit)

# ---Um Aluno---# OK!
@app.get("/alunos/{aluno_id}", response_model=schemas.Aluno)
def aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

# ---Todas as Disciplinas---# OK!
@app.get("/alunos/{aluno_id}/disciplinas/")
def todas_disciplinas( db:Session ,aluno_id: int ,skip: int = 0 ,limit: int = 100):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.get_disciplinas(db ,aluno_id=aluno_id ,skip=skip, limit=limit)

# ---Todos os Nomes de Disciplinas ---# OK!
@app.get("/alunos/{aluno_id}/disciplinas/nomes")
def todos_nomes_disciplinas(db:Session,aluno_id: int ,skip: int = 0 ,limit: int = 100):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.get_nomes_disciplinas(db ,aluno_id=aluno_id ,skip=skip ,limit=limit)

#---Todas as Anotações de uma Matéria Especifica ---#
@app.get("/alunos/{aluno_id}/disciplinas/{disciplina_id}/anotacoes")
def todas_anotacoes_disciplina(db:Session,aluno_id: int, disciplina_id: int=None):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno is None:
        if db_disciplina is None:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.get_anotacoes(db=db, aluno=aluno_id ,disciplina=disciplina_id)

#---Todas as Notas de uma Matéria Especifica ---#
@app.get("/alunos/{aluno_id}/disciplinas/{disciplina_id}/notas")
def todas_notas_disciplina(db:Session,aluno_id: int,disciplina_id: int):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno is None:
        if db_disciplina is None:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.get_notas(db=db, aluno=aluno_id ,disciplina=disciplina_id)

#---Altera disciplina---#
@app.patch("/alunos/{aluno_id}/disciplinas/{disciplina_id}/nome/disciplina", response_model= schemas.Disciplina)
def altera_nome_disciplina(db:Session,aluno_id:int ,disciplina_id: int, nome_disciplina: schemas.Disciplina):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno is None:
        if db_disciplina is None:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.alter_disc_nome(db=db,disciplina=disciplina_id,novo_nome=nome_disciplina)

#---Altera disciplina Nota---#
@app.patch("/alunos/{aluno_id}/disciplinas/{disciplina_id}/notas/{id_nota}", response_model= schemas.Nota)
def altera_nota_disciplina(db:Session,aluno_id:int ,disciplina_id: int,id_nota:int ,nome_nota: schemas.Nota):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno is None:
        if db_disciplina is None:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.alter_nota(db=db,nota_id=id_nota,nova_nota=nome_nota)

#---Deletar Nota ---#
@app.delete("/alunos/{aluno_id}/disciplinas/{disciplina_id}/notas/{id_nota}/deleta")
def delete_nota(db:Session,aluno_id:int ,disciplina_id: int, id_nota: int):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno is None:
        if db_disciplina is None:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.delete_nota(db=db,nota_id=id_nota)

#---Deletar disciplina ---#
@app.delete("/alunos/{aluno_id}/disciplina/{disciplina_id}")
def delete_disciplina(db:Session,aluno_id:int ,disciplina_id: int):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    db_disciplina = crud.get_disciplina(db,disciplina_id=disciplina_id)
    if db_aluno is None:
        if db_disciplina is None:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return crud.delete_disciplina(db=db,disciplina=disciplina_id)

