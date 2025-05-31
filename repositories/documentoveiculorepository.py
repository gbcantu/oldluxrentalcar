from sqlalchemy.orm import Session
from src.database.session import get_db
from src.entities.documentoveiculo import DocumentoVeiculo
from decimal import Decimal
from datetime import date

def get_all_documentoveiculos():
    db = next(get_db())
    try:
        return db.query(DocumentoVeiculo).all()
    finally:
        db.close()

def get_documentoveiculo(documentoveiculo_id: int) -> DocumentoVeiculo:
    db: Session = next(get_db())
    
    documentoveiculo = db.query(DocumentoVeiculo).get(documentoveiculo_id)
    
    return documentoveiculo

def get_documentoveiculo_by_veiculo_id(veiculo_id: int) -> DocumentoVeiculo:
    db: Session = next(get_db())
    documentoveiculo = db.query(DocumentoVeiculo).filter(DocumentoVeiculo.veiculo_id == veiculo_id).all()
    return documentoveiculo

def add_documentoveiculo(veiculo_id: int, tipo_documento: str, numero_documento: str, validade_inicio: date, validade_fim: date, 
                         observacoes: str) -> DocumentoVeiculo:
    db: Session = next(get_db())
    
    documentoveiculo = DocumentoVeiculo(veiculo_id=veiculo_id, tipo_documento=tipo_documento, numero_documento=numero_documento, 
                                        validade_inicio=validade_inicio, validade_fim=validade_fim, observacoes=observacoes)
    db.add(documentoveiculo)
    db.commit()
    db.refresh(documentoveiculo)
    
    return documentoveiculo

def update_documentoveiculo(id: int, veiculo_id: int, tipo_documento: str, numero_documento: str, validade_inicio: date, validade_fim: date, observacoes: str):
    db = next(get_db())
    try:
        documentoveiculo = db.query(DocumentoVeiculo).get(id)
        if not documentoveiculo:
            return None
        
        documentoveiculo.veiculo_id = veiculo_id
        documentoveiculo.tipo_documento = tipo_documento
        documentoveiculo.numero_documento = numero_documento
        documentoveiculo.validade_inicio = validade_inicio
        documentoveiculo.validade_fim = validade_fim
        documentoveiculo.observacoes = observacoes
        
        db.commit()
        db.refresh(documentoveiculo)
        
        return documentoveiculo
    finally:
        db.close()

def delete_documentoveiculo(id: int):
    db = next(get_db())
    try:
        documentoveiculo = db.query(DocumentoVeiculo).get(id)
        if not documentoveiculo:
            return False
        
        db.delete(documentoveiculo)
        db.commit()
        return True
    finally:
        db.close()