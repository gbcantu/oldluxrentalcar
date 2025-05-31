import re
from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date
from sqlalchemy.exc import OperationalError
from src.services.documentoveiculoservice import (
    getAllDocumentoveiculo,
    getDocumentoveiculo,
    getDocumentoveiculoByVeiculoId,
    addDocumentoveiculo,
    updateDocumentoveiculo,
    deleteDocumentoveiculo
)

class DocumentoveiculoResponseSchema(BaseModel):
    id: int
    veiculo_id: int
    tipo_documento: str
    numero_documento: str
    validade_inicio: date
    validade_fim: date
    observacoes: str

class DocumentoveiculoRequestSchema(BaseModel):
    veiculo_id: int
    tipo_documento: str
    numero_documento: str
    validade_inicio: date
    validade_fim: date
    observacoes: str

    @validator("validade_inicio")
    def validate_validade_inicio(cls, value):
        # Verifica se a data de validade_inicio não é superior ao dia de hoje
        if value > date.today():
            raise ValueError("A data de validade de início não pode ser posterior ao dia de hoje.")
        return value

    @validator("validade_fim")
    def validate_validade_fim(cls, value, values):
        # Verifica se validade_fim não é anterior a validade_inicio
        if 'validade_inicio' in values and value < values['validade_inicio']:
            raise ValueError("A data de validade de fim não pode ser anterior à data de validade de início.")
        return value

    @validator("observacoes")
    def validate_observacoes(cls, value):
        # Verifica se observacoes contém apenas caracteres alfanuméricos e espaços
        if not re.match(r"^[a-zA-Z0-9\sáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ.,;:!?()-]+$", value):
            raise ValueError("Observações devem conter apenas caracteres alfanuméricos, espaços e pontuações básicas.")
        return value.strip()

    @validator("tipo_documento")
    def validate_tipo_documento(cls, value):
        tipos_validos = ["Licenciamento", "Seguro", "CRLV", "IPVA", "Multa"]
        if value not in tipos_validos:
            raise ValueError(f"Tipo de documento inválido. Deve ser um dos: {', '.join(tipos_validos)}")
        return value

    @validator("numero_documento")
    def validate_numero_documento(cls, value):
        if not re.match(r"^[A-Za-z0-9-]+$", value):
            raise ValueError("Número do documento deve conter apenas letras, números e hífens")
        return value.strip()

def get_documentoveiculo_item(documentoveiculo_id: int) -> Optional[DocumentoveiculoResponseSchema]:
    try:
        documentoveiculo = getDocumentoveiculo(documentoveiculo_id)
        return documentoveiculo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar Documento Veiculo: {str(e)}"
        )
    
def get_documentoveiculo_by_veiculo_id(veiculo_id: int) -> List[DocumentoveiculoResponseSchema]:
    try:
        documentoveiculo = getDocumentoveiculoByVeiculoId(veiculo_id)
        return documentoveiculo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar manutenções do veículo: {str(e)}"
        )


def put_documentoveiculo_item(documentoveiculo_id: int, data: DocumentoveiculoRequestSchema) -> DocumentoveiculoResponseSchema:
    documentoveiculo = updateDocumentoveiculo(id=documentoveiculo_id, **data.dict())
    
    if not documentoveiculo:
        raise HTTPException(status_code=404, detail="Documento do Veiculo não encontrado")
    
    return documentoveiculo
    
def delete_documentoveiculo_item(id: int) -> DocumentoveiculoResponseSchema:
    documentoveiculo = getDocumentoveiculo(id)
    if not documentoveiculo:
        raise HTTPException(status_code=404, detail="Documento do Veiculo não encontrado")
    
    if not deleteDocumentoveiculo(id):
        raise HTTPException(status_code=500, detail="Erro ao remover o Documento do Veiculo")
    
    return documentoveiculo

def get_documentoveiculo_list() -> List[DocumentoveiculoResponseSchema]:
    try:
        return getAllDocumentoveiculo()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_documentoveiculo_item(data: DocumentoveiculoRequestSchema) -> DocumentoveiculoResponseSchema:
    try:
        documentoveiculo = addDocumentoveiculo(**data.dict())
        return documentoveiculo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
