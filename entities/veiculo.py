from sqlalchemy import Column, Integer, String, Boolean, Numeric
from src.entities.base import Base

class Veiculo(Base):
    __tablename__ = "veiculo"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(100), nullable=False)
    marca = Column(String(100), nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    placa = Column(String(10), unique=True, nullable=False)
    valor_diaria = Column(Numeric(10, 2), nullable=False)
    quilometragem_atual = Column(Integer, nullable=False)
    disponivel = Column(Boolean, nullable=False)