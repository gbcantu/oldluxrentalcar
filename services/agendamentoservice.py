from src.repositories.agendamentorepository import (
    get_all_agendamentos, 
    get_agendamento, 
    get_agendamento_by_veiculo_id, 
    get_agendamento_by_cliente_id, 
    add_agendamento, 
    update_agendamento, 
    delete_agendamento
)
from src.entities.agendamento import Agendamento
from src.services.veiculoservice import getVeiculo
from src.services.clienteservice import getCliente
from marshmallow import ValidationError
from decimal import Decimal
from datetime import date

def getAllAgendamento():
    return get_all_agendamentos()

def getAgendamento(cliente_id):
    return get_agendamento(cliente_id)

def getAgendamentoByVeiculoId(veiculo_id: int):
    return get_agendamento_by_veiculo_id(veiculo_id)

def getAgendamentoByClienteId(cliente_id: int):
    return get_agendamento_by_cliente_id(cliente_id)

def validar_agendamento_periodo(veiculo_id: int, data_inicio: date, data_fim: date):
    veiculo = getVeiculo(veiculo_id)
    if not veiculo:
        raise ValueError("Veículo não encontrado")
    if not veiculo.disponivel:
        raise ValueError("Veículo não está disponível para locação")

    if data_inicio < date.today():
        raise ValueError("Data de início não pode ser no passado")
    
    if data_fim <= data_inicio:
        raise ValueError("Data de término deve ser após a data de início")
    

    agendamentos = get_agendamento_by_veiculo_id(veiculo_id)
    for agendamento in agendamentos:
        if agendamento.status in ["agendado", "em_andamento"]:
            if not (data_fim < agendamento.data_inicio or data_inicio > agendamento.data_fim):
                raise ValueError(f"Veículo já possui agendamento ativo no período de {agendamento.data_inicio} a {agendamento.data_fim}")

def addAgendamento(cliente_id: int, veiculo_id: int, data_inicio: date, data_fim: date,
                  valor_total: Decimal, quilometragem_retirada: int,
                  quilometragem_devolucao: int, status: str) -> Agendamento:
    
    if not status:
        raise ValidationError("Status não pode ser vazio.")
    
    if quilometragem_devolucao < quilometragem_retirada:
        raise ValueError("Quilometragem de devolução não pode ser menor que a de retirada")
    
    validar_agendamento_periodo(veiculo_id, data_inicio, data_fim)

    veiculo = getVeiculo(veiculo_id)
    if quilometragem_retirada < veiculo.quilometragem_atual:
        raise ValueError(f"Quilometragem de retirada ({quilometragem_retirada}) não pode ser menor que a atual do veículo ({veiculo.quilometragem_atual})")
    
    return add_agendamento(cliente_id=cliente_id,veiculo_id=veiculo_id,data_inicio=data_inicio,
        data_fim=data_fim,valor_total=valor_total,quilometragem_retirada=quilometragem_retirada,
        quilometragem_devolucao=quilometragem_devolucao,status=status)

def updateAgendamento(id: int, cliente_id: int, veiculo_id: int, data_inicio: date, data_fim: date,
                    valor_total: Decimal, quilometragem_retirada: int,
                    quilometragem_devolucao: int, status: str):
    
    return update_agendamento(id, cliente_id, veiculo_id, data_inicio,
                            data_fim, valor_total, quilometragem_retirada,
                            quilometragem_devolucao, status)

def deleteAgendamento(id: int) -> bool:
    return delete_agendamento(id)
