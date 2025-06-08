from sqlalchemy.orm import Session
from src.database.session import get_db
from src.entities.agendamento import Agendamento
from decimal import Decimal
from datetime import date

def get_all_agendamentos():
    db = next(get_db())
    try:
        return db.query(Agendamento).all()
    finally:
        db.close()

def get_agendamento_by_veiculo_id(veiculo_id: int) -> Agendamento:
    db: Session = next(get_db())
    agendamento = db.query(Agendamento).filter(Agendamento.veiculo_id == veiculo_id).all()
    return agendamento

def get_agendamento_by_cliente_id(cliente_id: int) -> Agendamento:
    db: Session = next(get_db())
    agendamento = db.query(Agendamento).filter(Agendamento.cliente_id == cliente_id).all()
    return agendamento

def get_agendamento(agendamento_id: int) -> Agendamento:
    db: Session = next(get_db())
    
    agendamento = db.query(Agendamento).get(agendamento_id)
    
    return agendamento

def add_agendamento(cliente_id: int, veiculo_id: int, data_inicio: date, data_fim: date,
                    valor_total: Decimal, quilometragem_retirada: int,
                    quilometragem_devolucao: int, status: str) -> Agendamento:
    db: Session = next(get_db())
    
    agendamento = Agendamento(cliente_id=cliente_id, veiculo_id=veiculo_id, data_inicio=data_inicio,
                            data_fim=data_fim, valor_total=valor_total, quilometragem_retirada=quilometragem_retirada,
                            quilometragem_devolucao=quilometragem_devolucao, status=status)
    db.add(agendamento)
    db.commit()
    db.refresh(agendamento)
    
    return agendamento

def update_agendamento(id: int, cliente_id: int, veiculo_id: int, data_inicio: date, data_fim: date,
                    valor_total: Decimal, quilometragem_retirada: int,
                    quilometragem_devolucao: int, status: str):
    db = next(get_db())
    try:
        agendamento = db.query(Agendamento).get(id)
        if not agendamento:
            return None
        
        agendamento.cliente_id = cliente_id
        agendamento.veiculo_id = veiculo_id
        agendamento.data_inicio = data_inicio
        agendamento.data_fim = data_fim
        agendamento.valor_total = valor_total
        agendamento.quilometragem_retirada = quilometragem_retirada
        agendamento.quilometragem_devolucao = quilometragem_devolucao
        agendamento.status = status
        
        db.commit()
        db.refresh(agendamento)
        return agendamento
    finally:
        db.close()

def delete_agendamento(id: int):
    db = next(get_db())
    try:
        agendamento = db.query(Agendamento).get(id)
        if not agendamento:
            return False
        
        db.delete(agendamento)
        db.commit()
        return True
    finally:
        db.close()

def get_status_agendamento(id: int) -> str:
    db: Session = next(get_db())
    try:
        agendamento = db.query(Agendamento).get(id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado")
        return agendamento.status
    finally:
        db.close()

def update_agendamento_status_concluido(agendamento_id: int, quilometragem_devolucao: int) -> Agendamento:
    db: Session = next(get_db())
    try:
        agendamento = db.query(Agendamento).get(agendamento_id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado")
        
        agendamento.status = "concluido"
        agendamento.quilometragem_devolucao = quilometragem_devolucao

        db.commit()
        db.refresh(agendamento)
        return agendamento
    finally:
        db.close()