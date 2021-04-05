from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Aluno(Base):

    __tablename__ = "alunos"


    id = Column(String, primary_key=True, index=True)
    nome = Column(String, index=True)
    senha = Column(String)
    logado = Column(Boolean, default=True)

    disciplinas = relationship("Disciplinas", back_populates="disciplina")
    notas = relationship("Notas", back_populates="nota_aluno")

class Disciplinas(Base):

    __tablename__ = "disciplinas"

    id = Column(String, primary_key=True, index=True)
    nome_disciplina = Column(String, index=True)
    nome_professor = Column(String)
    anotacoes = Column(String)
    alunos_id = Column(String, ForeignKey("alunos.id"))

    disciplina = relationship("Alunos", back_populates="disciplinas")
    notas = relationship("Notas",back_populates="nota_disciplina")

class Notas(Base):

    __tablename__ = "notas"

    id = Column(String, primary_key=True, index=True)
    nome_da_prova = Column(String, index=True)
    nota = Column(Integer)
    disciplina_id = Column(String, ForeignKey("disciplinas.id"))
    aluno_id = Column(String, ForeignKey("alunos.id"))

    nota_disciplina = relationship("Disciplinas", back_populates="notas")
    nota_aluno = relationship("Alunos", back_populates="notas")
