from sqlalchemy.orm import Session
from src.database.session import get_db
from src.entities.veiculo import Veiculo
from decimal import Decimal

def get_all_veiculos():
    db = next(get_db())
    try:
        return db.query(Veiculo).all()
    finally:
        db.close()

def get_veiculo(veiculo_id: int) -> Veiculo:
    db: Session = next(get_db())
    
    veiculo = db.query(Veiculo).get(veiculo_id)
    
    return veiculo

def add_veiculo(modelo: str, marca: str, ano_fabricacao: int, placa: str, valor_diaria: Decimal, quilometragem_atual: int, disponivel: bool) -> Veiculo:
    db: Session = next(get_db())
    
    veiculo = Veiculo(modelo=modelo, marca=marca, ano_fabricacao=ano_fabricacao, placa=placa, valor_diaria=valor_diaria, 
                      quilometragem_atual=quilometragem_atual, disponivel=disponivel)
    db.add(veiculo)
    db.commit()
    db.refresh(veiculo)
    
    return veiculo

def update_veiculo(id: int, modelo: str, marca: str, ano_fabricacao: int, placa: str, valor_diaria: Decimal, quilometragem_atual: int, disponivel: bool):
    db = next(get_db())
    try:
        veiculo = db.query(Veiculo).get(id)
        if not veiculo:
            return None
        
        veiculo.modelo = modelo
        veiculo.marca = marca
        veiculo.ano_fabricacao = ano_fabricacao
        veiculo.placa = placa
        veiculo.valor_diaria = valor_diaria
        veiculo.quilometragem_atual = quilometragem_atual
        veiculo.disponivel = disponivel
        
        db.commit()
        db.refresh(veiculo)
        
        return veiculo
    finally:
        db.close()

def delete_veiculo(id: int):
    db = next(get_db())
    try:
        veiculo = db.query(Veiculo).get(id)
        if not veiculo:
            return False
        
        db.delete(veiculo)
        db.commit()
        return True
    finally:
        db.close()