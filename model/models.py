from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Tarefas(Base):
    __tablename__ = 'tarefas'
    id = Column(Integer, primary_key=True)
    tarefa = Column(Text)
    status = Column(String(255))