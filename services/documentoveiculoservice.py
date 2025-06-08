from marshmallow import ValidationError
from datetime import date
from src.entities.documentoveiculo import DocumentoVeiculo
from src.repositories.documentoveiculorepository import (
    get_all_documentoveiculos, 
    get_documentoveiculo,
    get_documentoveiculo_by_veiculo_id, 
    add_documentoveiculo, 
    update_documentoveiculo, 
    delete_documentoveiculo
)

def getAllDocumentoveiculo():
    return get_all_documentoveiculos()

def getDocumentoveiculo(documentoveiculo_id):
    return get_documentoveiculo(documentoveiculo_id)

def getDocumentoveiculoByVeiculoId(veiculo_id: int):
    return get_documentoveiculo_by_veiculo_id(veiculo_id)

def addDocumentoveiculo(veiculo_id: int, tipo_documento: str, numero_documento: str, validade_inicio: date, validade_fim: date, 
                         observacoes: str) -> DocumentoVeiculo:
    if not tipo_documento:
        raise ValidationError("O tipo do documento não pode ser vazio.")
    if not numero_documento:
        raise ValidationError("O número do documento não pode ser vazio.")
    if not validade_inicio:
        raise ValidationError("O documento não pode ter data de inicio vazia.")
    if not validade_fim:
        raise ValidationError("O documento não pode ter data do fim vazia.")
    
    return add_documentoveiculo(veiculo_id=veiculo_id, tipo_documento=tipo_documento, numero_documento=numero_documento, validade_inicio=validade_inicio,
                       validade_fim=validade_fim,observacoes=observacoes)

def updateDocumentoveiculo(id: int, veiculo_id: int, tipo_documento: str, numero_documento: str, validade_inicio: date, validade_fim: date, 
                  observacoes: str):
    return update_documentoveiculo(id, veiculo_id, tipo_documento, numero_documento, validade_inicio, validade_fim, observacoes)

def deleteDocumentoveiculo(id: int) -> bool:
    return delete_documentoveiculo(id)