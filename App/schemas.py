from typing import List, Optional
from pydantic import BaseModel, Field

class NotaEntry(BaseModel):
    nome_da_prova : str
    nota   :   int
class NotaCreate(NotaEntry):
    pass
class Nota(NotaEntry):
    id: int
    aluno_id: int
    disciplina_id: int
    class Config:
        orm_mode = True

class DisciplinaEntry(BaseModel):
    nome_disciplina  :  str           = Field(..., example="Mega Dados")
    nome_professor   :  Optional[str] = Field(..., example="Fabio Ayres")
    anotacoes        :  Optional[str] = Field(..., example="Fazer projeto SQL,")
class DisciplinaCreate(DisciplinaEntry):
    pass
class Disciplina(DisciplinaEntry):
    id: int
    notas: List[NotaEntry] = []
    alunos_id: List[int]
    class Config:
        orm_mode = True

class AlunoEntry(BaseModel):
    nome:   str = Field(..., example="José")
class AlunoCreate(AlunoEntry):
    senha:  str
class Aluno(AlunoEntry):
    id:     int
    logado: bool
    disciplinas: List[Disciplina] = []
    notas: List[Nota] = []
    class Config:
        orm_mode = True