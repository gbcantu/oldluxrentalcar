from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from src.entities.base import Base

class Manutencao(Base):
    __tablename__ = "manutencao"

    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(Integer, ForeignKey('veiculo.id'), nullable=False)
    tipo = Column(String(50), nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String)
    custo = Column(Numeric(10, 2), nullable=False)
    quilometragem = Column(Integer, nullable=False)
