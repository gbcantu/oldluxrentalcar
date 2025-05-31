from src.repositories.manutencaorepository import (
    get_all_manutencoes, 
    get_manutencao,
    get_manutencoes_by_veiculo_id, 
    add_manutencao, 
    update_manutencao, 
    delete_manutencao
)
from src.entities.manutencao import Manutencao
from marshmallow import ValidationError
from datetime import date
from decimal import Decimal

def getAllManutencao():
    return get_all_manutencoes()

def getManutencao(manutencao_id):
    return get_manutencao(manutencao_id)

def getManutencoesByVeiculoId(veiculo_id: int):
    return get_manutencoes_by_veiculo_id(veiculo_id)

def addManutencao(veiculo_id: int,tipo: str, data: date, descricao:str, 
                   custo: Decimal, quilometragem: int) -> Manutencao:
    if not tipo:
        raise ValidationError("tipo não pode ser vazio.")
    if not custo:
        raise ValidationError("custo não pode ser vazio.")
    
    return add_manutencao(veiculo_id=veiculo_id,tipo=tipo, data=data, 
                            descricao=descricao, custo=custo, 
                            quilometragem=quilometragem)

def updateManutencao(id: int,veiculo_id:int, tipo: str, data: date, descricao:str, 
                   custo: Decimal, quilometragem: int):
    return update_manutencao(id,veiculo_id, tipo, data, descricao, custo, quilometragem)

def deleteManutencao(id: int) -> bool:
    return delete_manutencao(id)