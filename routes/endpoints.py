from fastapi import APIRouter, Path
from typing import List
from src.controller.clientecontroller import (
    ClienteResponseSchema,
    ClienteRequestSchema,
    get_cliente_item,
    put_cliente_item,
    delete_cliente_item,
    get_cliente_list,
    post_cliente_item,
)
from src.controller.veiculocontroller import (
    VeiculoResponseSchema,
    VeiculoRequestSchema,
    get_veiculo_item,
    put_veiculo_item,
    delete_veiculo_item,
    get_veiculo_list,
    post_veiculo_item,
)

# Criando um único APIRouter
router = APIRouter()

#ENDPOINTS CLIENTES
@router.get("/clientes/", response_model=List[ClienteResponseSchema])
def list_clientes():
    return get_cliente_list()

@router.post("/clientes/", response_model=ClienteResponseSchema, status_code=201)
def create_cliente(data: ClienteRequestSchema):
    return post_cliente_item(data)

@router.get("/clientes/{cliente_id}", response_model=ClienteResponseSchema)
def get_cliente(cliente_id: int = Path(..., gt=0)):
    return get_cliente_item(cliente_id)

@router.put("/clientes/{cliente_id}", response_model=ClienteResponseSchema, status_code=201)
def update_cliente(cliente_id: int, data: ClienteRequestSchema):
    return put_cliente_item(cliente_id, data)

@router.delete("/clientes/{cliente_id}", response_model=ClienteResponseSchema)
def delete_cliente(cliente_id: int = Path(..., gt=0)):
    return delete_cliente_item(cliente_id)

#ENDPOINTS VEICULOS
@router.get("/veiculos/", response_model=List[VeiculoResponseSchema])
def list_veiculos():
    return get_veiculo_list()

@router.post("/veiculos/", response_model=VeiculoResponseSchema, status_code=201)
def create_veiculo(data: VeiculoRequestSchema):
    return post_veiculo_item(data)

@router.get("/veiculos/{veiculo_id}", response_model=VeiculoResponseSchema)
def get_veiculo(veiculo_id: int = Path(..., gt=0)):
    return get_veiculo_item(veiculo_id)

@router.put("/veiculos/{veiculo_id}", response_model=VeiculoResponseSchema, status_code=201)
def update_veiculo(veiculo_id: int, data: VeiculoRequestSchema):
    return put_veiculo_item(veiculo_id, data)

@router.delete("/veiculos/{veiculo_id}", response_model=VeiculoResponseSchema)
def delete_veiculo(veiculo_id: int = Path(..., gt=0)):
    return delete_veiculo_item(veiculo_id)

# Função para inicializar os endpoints no app
def initialize_endpoints(app):
    app.include_router(router)
