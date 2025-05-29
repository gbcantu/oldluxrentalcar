from src.repositories.clienterepository import (
    get_all_clientes, 
    get_cliente, 
    add_cliente, 
    update_cliente, 
    delete_cliente
)
from src.entities.cliente import Cliente
from marshmallow import ValidationError

def getAllCliente():
    return get_all_clientes()

def getCliente(cliente_id):
    return get_cliente(cliente_id)

def addCliente(nome: str, cpf: str, email: str, telefone: str) -> Cliente:
    if not nome:
        raise ValidationError("Nome não pode ser vazio.")
    
    return add_cliente(nome=nome, cpf=cpf, email=email, telefone=telefone)

def updateCliente(id: int, nome: str, cpf: str, email: str, telefone: str):
    return update_cliente(id, nome, cpf, email, telefone)

def deleteCliente(id: int) -> bool:
    return delete_cliente(id)