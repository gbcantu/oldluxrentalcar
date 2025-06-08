import re
from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List
from decimal import Decimal
from datetime import date
from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError
from src.services.agendamentoservice import (
    getAllAgendamento,
    getAgendamento,
    getAgendamentoByVeiculoId,
    getAgendamentoByClienteId,
    addAgendamento,
    updateAgendamento,
    deleteAgendamento,
    updateconcluirAgendamento,
)
from src.services.clienteservice import getCliente
from src.services.veiculoservice import getVeiculo

class AgendamentoResponseSchema(BaseModel):
    id: int
    cliente_id: int
    veiculo_id: int
    data_inicio: date
    data_fim: date
    valor_total: Decimal
    quilometragem_retirada: int
    quilometragem_devolucao: int
    status: str

class AgendamentoRequestSchema(BaseModel):
    cliente_id: int
    veiculo_id: int
    data_inicio: date
    data_fim: date
    quilometragem_retirada: int
    quilometragem_devolucao: int
    status: str


    @validator("data_inicio")
    def validate_data_inicio(cls, value):
        if value < date.today():
            raise ValueError("Não são permitidos agendamentos com datas retroativas")
        return value
    
    @validator("data_fim")
    def validate_data_fim(cls, value, values):
        if "data_inicio" in values and value < values["data_inicio"]:
            raise ValueError("A data de término não pode ser anterior à data de início")
        return value
    
    @validator("quilometragem_devolucao")
    def validate_quilometragem_devolucao(cls, value, values):
        if "quilometragem_retirada" in values and value < values["quilometragem_retirada"]:
            raise ValueError("A quilometragem de devolução não pode ser menor que a de retirada")
        return value
    
    @validator("status")
    def validate_status(cls, value):
        valid_statuses = ["agendado", "em_andamento", "concluido", "cancelado"]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status inválido. Os status válidos são: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validator("veiculo_id")
    def validate_veiculo_disponivel(cls, value, values):
        if "data_inicio" in values and "data_fim" in values:
            agendamentos = getAgendamentoByVeiculoId(value)
            for agendamento in agendamentos:
                if not (values["data_fim"] < agendamento.data_inicio or values["data_inicio"] > agendamento.data_fim):
                    if agendamento.status in ["agendado", "em_andamento"]:
                        raise ValueError("Veículo não está disponível no período solicitado")
        return value

def get_agendamento_item(agendamento_id: int) -> Optional[AgendamentoResponseSchema]:
    try:
        agendamento = getAgendamento(agendamento_id)
        return agendamento
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar agendamento: {str(e)}"
        )

def put_agendamento_item(agendamento_id: int, data: AgendamentoRequestSchema) -> AgendamentoResponseSchema:
    try:
        cliente = getCliente(data.cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        veiculo = getVeiculo(data.veiculo_id)
        if not veiculo:
            raise ValueError("Veículo não encontrado")
        
        dias_alugados = (data.data_fim - data.data_inicio).days
        if dias_alugados <= 0:
            raise ValueError("Período de locação inválido")
        
        valor_total = Decimal(str(veiculo.valor_diaria)) * dias_alugados
        
        agendamento = updateAgendamento(
            id=agendamento_id,
            cliente_id=data.cliente_id,
            veiculo_id=data.veiculo_id,
            data_inicio=data.data_inicio,
            data_fim=data.data_fim,
            valor_total=valor_total,
            quilometragem_retirada=data.quilometragem_retirada,
            quilometragem_devolucao=data.quilometragem_devolucao,
            status=data.status
        )

        return agendamento

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar agendamento: {str(e)}"
        )
    
def get_agendamento_by_veiculo_id(veiculo_id: int) -> List[AgendamentoResponseSchema]:
    try:
        agendamento = getAgendamentoByVeiculoId(veiculo_id)
        return agendamento
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar manutenções do veículo: {str(e)}"
        )
    
def get_agendamento_by_cliente_id(cliente_id: int) -> List[AgendamentoResponseSchema]:
    try:
        agendamento = getAgendamentoByClienteId(cliente_id)
        return agendamento
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar manutenções do veículo: {str(e)}"
        )
    
def delete_agendamento_item(id: int) -> AgendamentoResponseSchema:
    agendamento = getAgendamento(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    if not deleteAgendamento(id):
        raise HTTPException(status_code=500, detail="Erro ao remover agendamento")
    
    return agendamento

def get_agendamento_list() -> List[AgendamentoResponseSchema]:
    try:
        return getAllAgendamento()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_agendamento_item(data: AgendamentoRequestSchema) -> AgendamentoResponseSchema:
    try:
        cliente = getCliente(data.cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        veiculo = getVeiculo(data.veiculo_id)
        if not veiculo:
            raise ValueError("Veículo não encontrado")
        
        dias_alugados = (data.data_fim - data.data_inicio).days
        if dias_alugados <= 0:
            raise ValueError("Período de locação inválido")
        
        valor_total = Decimal(str(veiculo.valor_diaria)) * dias_alugados
        
        agendamento = addAgendamento(
            cliente_id=data.cliente_id,
            veiculo_id=data.veiculo_id,
            data_inicio=data.data_inicio,
            data_fim=data.data_fim,
            valor_total=valor_total,
            quilometragem_retirada=data.quilometragem_retirada,
            quilometragem_devolucao=data.quilometragem_devolucao,
            status=data.status
        )
        
        return agendamento
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar agendamento: {str(e)}"
        )
    
def concluir_agendamento_item(agendamento_id: int, quilometragem_devolucao: int):
    return updateconcluirAgendamento(agendamento_id, quilometragem_devolucao)