from sqlalchemy.orm import Session
from src.database.session import get_db
from src.entities.manutencao import Manutencao
from datetime import date
from decimal import Decimal


def get_all_manutencoes():
    db = next(get_db())
    try:
        return db.query(Manutencao).all()
    finally:
        db.close()

def get_manutencao(manutencao_id: int) -> Manutencao:
    db: Session = next(get_db())
    
    manutencao = db.query(Manutencao).get(manutencao_id)
    
    return manutencao

def get_manutencoes_by_veiculo_id(veiculo_id: int) -> Manutencao:
    db: Session = next(get_db()) 
    manutencoes = db.query(Manutencao).filter(Manutencao.veiculo_id == veiculo_id).all()
    return manutencoes


def add_manutencao(veiculo_id: int, tipo:str, data: date, descricao:str, 
                   custo: Decimal, quilometragem: int) -> Manutencao:
    db: Session = next(get_db())
    
    manutencao = Manutencao(veiculo_id=veiculo_id, tipo=tipo, data=data, 
                            descricao=descricao, custo=custo, 
                            quilometragem=quilometragem)
    db.add(manutencao)
    db.commit()
    db.refresh(manutencao)
    
    return manutencao

def update_manutencao(id: int,veiculo_id: int, tipo:str, data: date, descricao:str, 
                   custo: Decimal, quilometragem: int):
    db = next(get_db())
    try:
        manutencao = db.query(Manutencao).get(id)
        if not manutencao:
            return None
        manutencao.veiculo_id = veiculo_id
        manutencao.tipo = tipo
        manutencao.data = data
        manutencao.descricao = descricao
        manutencao.custo = custo
        manutencao.quilometragem = quilometragem
        
        db.commit()
        db.refresh(manutencao)
        return manutencao
    finally:
        db.close()

def delete_manutencao(id: int):
    db = next(get_db())
    try:
        manutencao = db.query(Manutencao).get(id)
        if not manutencao:
            return False
        
        db.delete(manutencao)
        db.commit()
        return True
    finally:
        db.close()