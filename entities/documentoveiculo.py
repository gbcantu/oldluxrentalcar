from sqlalchemy import Column, Integer, String, Date, ForeignKey
from src.entities.base import Base

class DocumentoVeiculo(Base):
    __tablename__ = "documentoveiculo"

    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(Integer, ForeignKey('veiculo.id'), nullable=False)
    tipo_documento = Column(String(50), nullable=False)
    numero_documento = Column(String(50), nullable=False)
    validade_inicio = Column(Date, nullable=False)
    validade_fim = Column(Date, nullable=False)
    observacoes = Column(String)