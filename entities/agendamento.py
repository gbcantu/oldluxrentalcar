from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from src.entities.base import Base

class Agendamento(Base):
    __tablename__ = "agendamento"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    veiculo_id = Column(Integer, ForeignKey('veiculo.id'), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    quilometragem_retirada = Column(Integer, nullable=False)
    quilometragem_devolucao = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)