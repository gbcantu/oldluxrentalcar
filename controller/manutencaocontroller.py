import re
from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date
from decimal import Decimal
from sqlalchemy.exc import OperationalError
from src.services.manutencaoservice import (
    getAllManutencao,
    getManutencao,
    getManutencoesByVeiculoId,
    addManutencao,
    updateManutencao,
    deleteManutencao
)

class ManutencaoResponseSchema(BaseModel):
    id: int 
    veiculo_id: int
    tipo: str
    data: date 
    descricao: str = None 
    custo: Decimal 
    quilometragem: int

class ManutencaoRequestSchema(BaseModel):
    veiculo_id: int
    tipo: str
    data: date 
    descricao: str = None
    custo: Decimal 
    quilometragem: int

    @validator("tipo")
    def validate_tipo(cls, value):
        if not re.match(r"^[a-zA-Z0-9_\s]+$", value):
            raise ValueError("Tipo deve conter apenas letras, números, espaços ou underscores.")
        return value.strip()

    @validator("data")
    def validate_data(cls, value):
        if value > date.today():
            raise ValueError("Data da manutenção não pode ser no futuro.")
        return value

    @validator("descricao")
    def validate_descricao(cls, value):
        if value and not re.match(r"^[\w\s.,\-áéíóúÁÉÍÓÚçÇàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛãõÃÕ]*$", value):
            raise ValueError("Descrição deve conter apenas letras, números, espaços e pontuação básica.")
        return value.strip() if value else value

    @validator("custo")
    def validate_custo(cls, value):
        if value <= 0:
            raise ValueError("Custo deve ser um valor positivo maior que zero.")
        return value

    @validator("quilometragem")
    def validate_quilometragem(cls, value):
        if value <= 0:
            raise ValueError("Quilometragem deve ser um valor positivo.")
        return value

def get_manutencao_item(manutencao_id: int) -> Optional[ManutencaoResponseSchema]:
    try:
        manutencao = getManutencao(manutencao_id)
        return manutencao
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar cliente: {str(e)}"
        )
    
def get_manutencao_by_veiculo_id(veiculo_id: int) -> List[ManutencaoResponseSchema]:
    try:
        manutencoes = getManutencoesByVeiculoId(veiculo_id)
        return manutencoes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar manutenções do veículo: {str(e)}"
        )

def put_manutencao_item(manutencao_id: int, data: ManutencaoRequestSchema) -> ManutencaoResponseSchema:
    manutencao = updateManutencao(id=manutencao_id, **data.dict())
    
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutencao não encontrado")
    
    return manutencao
    
def delete_manutencao_item(id: int) -> ManutencaoResponseSchema:
    manutencao = getManutencao(id)
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutencao não encontrado")
    
    if not deleteManutencao(id):
        raise HTTPException(status_code=500, detail="Erro ao remover cliente")
    
    return manutencao

def get_manutencao_list() -> List[ManutencaoResponseSchema]:
    try:
        return getAllManutencao()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_manutencao_item(data: ManutencaoRequestSchema) -> ManutencaoResponseSchema:
    try:
        manutencao = addManutencao(**data.dict())
        return manutencao
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
