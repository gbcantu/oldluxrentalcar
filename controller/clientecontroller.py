import re
from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List
from sqlalchemy.exc import OperationalError
from src.services.clienteservice import (
    updateCliente,
    getCliente,
    getAllCliente,
    addCliente,
    deleteCliente
)

class ClienteResponseSchema(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: str

class ClienteRequestSchema(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str

    @validator("nome")
    def validate_name(cls, value):
        if not re.match(r"^[a-zA-Z0-9_\s]+$", value):
            raise ValueError("Value must contain only alphanumeric and underscore characters.")
        return value

    @validator("cpf")
    def validate_cpf(cls, value):
        # remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, str(value)))
        
        # verifica se tem 11 dígitos
        if len(cpf) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos")
        
        # verifica se todos os dígitos são iguais (caso inválido)
        if len(set(cpf)) == 1:
            raise ValueError("CPF não pode ter todos os dígitos iguais")
        
        return value  # retorna o valor original (pode ser formatado ou não)

    @validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("E-mail não pode ser vazio")
        
        # validador e-mail
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("E-mail inválido")
        
        return value.strip().lower()  
    
    @validator("telefone")
    def validate_telefone(cls, value):
        telefone = ''.join(filter(str.isdigit, str(value)))
        
        # verifica se tem 10 (fixo) ou 11 (celular) digitos, incluindo DDD
        if len(telefone) not in (10, 11):
            raise ValueError("Telefone deve ter 10 (fixo) ou 11 (celular) dígitos")
        
        # formataçao opcional (ex: (21) 98765-4321)
        if len(telefone) == 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        else:  # Celular
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

def get_cliente_item(cliente_id: int) -> Optional[ClienteResponseSchema]:
    try:
        cliente = getCliente(cliente_id)
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar cliente: {str(e)}"
        )

def put_cliente_item(cliente_id: int, data: ClienteRequestSchema) -> ClienteResponseSchema:
    cliente = updateCliente(id=cliente_id, **data.dict())
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente
    
def delete_cliente_item(id: int) -> ClienteResponseSchema:
    cliente = getCliente(id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if not deleteCliente(id):
        raise HTTPException(status_code=500, detail="Erro ao remover cliente")
    
    return cliente

def get_cliente_list() -> List[ClienteResponseSchema]:
    try:
        return getAllCliente()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_cliente_item(data: ClienteRequestSchema) -> ClienteResponseSchema:
    try:
        cliente = addCliente(**data.dict())
        return cliente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
