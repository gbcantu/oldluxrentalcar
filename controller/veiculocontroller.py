import re
from decimal import Decimal
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List
from sqlalchemy.exc import OperationalError
from src.services.veiculoservice import (
    getAllVeiculo,
    getVeiculo,
    addVeiculo,
    updateVeiculo,
    deleteVeiculo
)

class VeiculoResponseSchema(BaseModel):
    id: int
    modelo: str
    marca: str
    ano_fabricacao: int
    placa: str
    valor_diaria: Decimal 
    quilometragem_atual: int
    disponivel: bool

class VeiculoRequestSchema(BaseModel):
    modelo: str
    marca: str
    ano_fabricacao: int
    placa: str
    valor_diaria: Decimal 
    quilometragem_atual: int
    disponivel: bool

    @validator("modelo")
    def validate_name(cls, value):
        if not re.match(r"^[a-zA-Z0-9_\s]+$", value):
            raise ValueError("O Modelo deve conter apenas caracteres letras e números.")
        return value


    @validator("marca")
    def validate_marca(cls, value):
        if not re.match(r"^[a-zA-Z0-9_\s]+$", value):
            raise ValueError("A Marca deve conter apenas caracteres letras e números.")
        return value
    
    @validator("ano_fabricacao")
    def validate_ano_fabricacao(cls, value):
        ano_atual = datetime.now().year
        if value > ano_atual:
            raise ValueError(f"O ano de fabricação não pode ser superior ao ano atual ({ano_atual})")
        if value < 1886:  # OBS: O primeiro carro foi fabricado em 1886 kkkk
            raise ValueError("Ano de fabricação inválido")
        return value
    
    @validator("placa")
    def validate_placa(cls, value):
        # Valida formato de placa (ex: ABC-1234 ou ABC1D23)
        pattern = r"^[A-Z]{3}-\d{4}$|^[A-Z]{3}\d{1}[A-Z0-9]{1}\d{2}$"
        value = value.strip().upper()
        if not re.match(pattern, value):
            raise ValueError("Placa inválida. O formato deve ser ABC-1234 ou ABC1D23")
        return value

    @validator("valor_diaria")
    def validate_valor_diaria(cls, value):
        if value <= 0:
            raise ValueError("O valor da diária deve ser maior que zero")
        return value

    @validator("quilometragem_atual")
    def validate_quilometragem(cls, value):
        if value < 0:
            raise ValueError("A quilometragem não pode ser negativa")
        return value

    @validator("disponivel")
    def validate_disponivel(cls, value):
        return value

def get_veiculo_item(veiculo_id: int) -> Optional[VeiculoResponseSchema]:
    try:
        veiculo = getVeiculo(veiculo_id)
        return veiculo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar cliente: {str(e)}"
        )

def put_veiculo_item(veiculo_id: int, data: VeiculoRequestSchema) -> VeiculoResponseSchema:
    veiculo = updateVeiculo(id=veiculo_id, **data.dict())
    
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")
    
    return veiculo
    
def delete_veiculo_item(id: int) -> VeiculoResponseSchema:
    veiculo = getVeiculo(id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")
    
    if not deleteVeiculo(id):
        raise HTTPException(status_code=500, detail="Erro ao remover veiculo")
    
    return veiculo

def get_veiculo_list() -> List[VeiculoResponseSchema]:
    try:
        return getAllVeiculo()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_veiculo_item(data: VeiculoRequestSchema) -> VeiculoResponseSchema:
    try:
        veiculo = addVeiculo(**data.dict())
        return veiculo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
