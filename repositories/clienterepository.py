from sqlalchemy.orm import Session
from src.database.session import get_db
from src.entities.cliente import Cliente

def get_all_clientes():
    db = next(get_db())
    try:
        return db.query(Cliente).all()
    finally:
        db.close()

def get_cliente(cliente_id: int) -> Cliente:
    db: Session = next(get_db())
    
    cliente = db.query(Cliente).get(cliente_id)
    
    return cliente

def get_cliente_by_cpf(cpf: str) -> Cliente:
    db: Session = next(get_db())
    return db.query(Cliente).filter(Cliente.cpf == cpf).first()

def add_cliente(nome: str, cpf: str, email: str, telefone: str) -> Cliente:
    db: Session = next(get_db())
    
    cliente = Cliente(nome=nome, cpf=cpf, email=email, telefone=telefone)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    
    return cliente

def update_cliente(id: int, nome: str, cpf: str, email: str, telefone: str):
    db = next(get_db())
    try:
        cliente = db.query(Cliente).get(id)
        if not cliente:
            return None
        
        cliente.nome = nome
        cliente.cpf = cpf
        cliente.email = email
        cliente.telefone = telefone
        
        db.commit()
        db.refresh(cliente)
        return cliente
    finally:
        db.close()

def delete_cliente(id: int):
    db = next(get_db())
    try:
        cliente = db.query(Cliente).get(id)
        if not cliente:
            return False
        
        db.delete(cliente)
        db.commit()
        return True
    finally:
        db.close()