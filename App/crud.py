from sqlalchemy.orm import Session

import models as models
import schemas as schemas

def get_alunos(db: Session):
    return db.query(models.Aluno).all()


def get_disciplinas(db: Session, aluno_id: int):
    return db.query(models.Disciplinas).filter(models.Aluno.alunos_id == aluno_id).all()

def get_disciplina(db: Session, disciplina_id: int):
    return db.query(models.Disciplinas).filter(models.Disciplinas.id==disciplina_id).all()

def get_nomes_disciplinas(db: Session, aluno_id: int):
    return db.query(models.Disciplinas.nome_disciplina).filter(models.Disciplinas.alunos_id == aluno_id).all()

def get_anotacoes(db: Session, aluno_id: int, disciplina_id: int):
    return db.query(models.Disciplinas.anotacoes).filter(models.Aluno.alunos_id == aluno_id and models.Disciplinas.id == disciplina_id).all()

def get_notas(db: Session, aluno_id: int, disciplina_id: int):
    return db.query(models.Notas).filter(models.Aluno.id == aluno_id and models.Disciplinas.id == disciplina_id).all()


def regiter_aluno(db: Session, aluno: schemas.AlunoCreate):
    password = aluno.senha + "PutAHashHere"
    db_aluno = models.Aluno(nome=aluno.nome, senha=password)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def regiter_nota(db: Session, aluno_id: int, disciplina_id: int, nota: schemas.NotaCreate):
    db_nota = models.Notas(aluno_id = aluno_id, disciplina_id = disciplina_id, nome_da_prova = nota.nome_da_prova, nota=nota.nota)
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

def alter_disc_nome(db: Session, disciplina_id: int, novo_nome: str):
    db_disc = db.query(models.Disciplinas).filter(models.Disciplinas.id == disciplina_id).first()
    db_disc.nome_disciplina = novo_nome
    db.commit(db_disc)
    db.refresh(db_disc)
    return db_disc

def alter_nota(db: Session,nota_id: int, nova_nota: int):
    db_nota_t = db.query(models.Notas).filter(models.Notas.id == nota_id).first()
    db_nota_t.nota = nova_nota
    db.commit(db_nota_t)
    db.refresh(db_nota_t)
    return db_nota_t

def delete_nota(db: Session,nota_id: int):
    return db.query(models.Notas.id==nota_id).delete()

def delete_disciplina(db: Session, disciplina_id: int):
    return db.query(models.Disciplinas.id==disciplina_id).delete()

""" def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item """
