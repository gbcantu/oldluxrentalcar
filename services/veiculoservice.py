from src.repositories.veiculorepository import (
    get_all_veiculos, 
    get_veiculo,
    get_veiculo_by_placa, 
    add_veiculo, 
    update_veiculo, 
    delete_veiculo
)
from src.entities.veiculo import Veiculo
from marshmallow import ValidationError
from decimal import Decimal

def getAllVeiculo():
    return get_all_veiculos()

def getVeiculo(veiculo_id):
    return get_veiculo(veiculo_id)

def addVeiculo(modelo: str, marca: str, ano_fabricacao: int, placa: str, valor_diaria: Decimal, quilometragem_atual: int, disponivel: bool) -> Veiculo:
    if not modelo:
        raise ValidationError("Nome não pode ser vazio.")
    if not marca:
        raise ValidationError("Marca não pode ser vazio.")
    if not placa:
        raise ValidationError("Placa não pode ser vazio.")
    
    if get_veiculo_by_placa(placa):  
        raise ValueError("Placa já cadastrada no sistema")
    
    return add_veiculo(modelo=modelo, marca=marca, ano_fabricacao=ano_fabricacao, placa=placa, valor_diaria=valor_diaria, 
                      quilometragem_atual=quilometragem_atual, disponivel=disponivel)

def updateVeiculo(id: int, modelo: str, marca: str, ano_fabricacao: int, placa: str, valor_diaria: Decimal, quilometragem_atual: int, disponivel: bool):
    if not modelo:
        raise ValidationError("Nome não pode ser vazio.")
    if not marca:
        raise ValidationError("Marca não pode ser vazio.")
    if not placa:
        raise ValidationError("Placa não pode ser vazio.")
    
    if get_veiculo_by_placa(placa):  
        raise ValueError("Placa já cadastrada no sistema")
    
    return update_veiculo(id, modelo, marca, ano_fabricacao, placa, valor_diaria, quilometragem_atual, disponivel)

def deleteVeiculo(id: int) -> bool:
    return delete_veiculo(id)