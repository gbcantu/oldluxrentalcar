from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.entities.base import Base 

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=True)
    
#   agendamentos = relationship("Agendamento", back_populates="cliente")