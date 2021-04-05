from typing import List, Optional
from pydantic import BaseModel, Field

class NotaEntry(BaseModel):
    nome_da_prova : str
    nota   :   int
class NotaCreate(NotaEntry):
    pass
class Nota(NotaEntry):
    id: str
    aluno_id: str
    disciplina_id: str
    class Config:
        orm_mode = True

class DisciplinaEntry(BaseModel):
    nome_disciplina  :  str           = Field(..., example="Mega Dados")
    nome_professor   :  Optional[str] = Field(..., example="Fabio Ayres")
    anotacoes        :  Optional[str] = Field(..., example="Fazer projeto SQL,")
class DisciplinaCreate(DisciplinaEntry):
    pass
class Disciplina(DisciplinaEntry):
    id: str
    notas: List[NotaEntry] = []
    alunos_id: List[str]
    class Config:
        orm_mode = True

class AlunoEntry(BaseModel):
    nome:   str = Field(..., example="José")
class AlunoCreate(AlunoEntry):
    senha:  str
class Aluno(AlunoEntry):
    id:     str
    logado: bool
    disciplinas: List[Disciplina] = []
    notas: List[Nota] = []
    class Config:
        orm_mode = True