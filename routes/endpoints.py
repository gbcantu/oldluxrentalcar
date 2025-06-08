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
from src.controller.agendamentocontroller import (
    AgendamentoResponseSchema,
    AgendamentoRequestSchema,
    get_agendamento_item,
    put_agendamento_item,
    delete_agendamento_item,
    get_agendamento_list,
    post_agendamento_item,
    get_agendamento_by_veiculo_id,
    get_agendamento_by_cliente_id,
    concluir_agendamento_item
)
from src.controller.documentoveiculocontroller import (
    DocumentoveiculoResponseSchema,
    DocumentoveiculoRequestSchema,
    get_documentoveiculo_item,
    get_documentoveiculo_by_veiculo_id,
    put_documentoveiculo_item,
    delete_documentoveiculo_item,
    get_documentoveiculo_list,
    post_documentoveiculo_item,
)
from src.controller.manutencaocontroller import (
    ManutencaoResponseSchema,
    ManutencaoRequestSchema,
    get_manutencao_item,
    get_manutencao_by_veiculo_id,
    put_manutencao_item,
    delete_manutencao_item,
    get_manutencao_list,
    post_manutencao_item,
)

# Criando um único APIRouter
router = APIRouter()

# ==============================
# ENDPOINTS INICIAL
# ==============================
@router.get("/")
def inicio():
    return {"mensagem": "Bem-vindo à API para gestão interna da OldLuxRentalCar!"}

# ==============================
# ENDPOINTS CLIENTES
# ==============================
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

# ==============================
# ENDPOINTS VEICULOS
# ==============================

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

# ==============================
# ENDPOINTS AGENDAMENTO
# ==============================

@router.get("/agendamentos/", response_model=List[AgendamentoResponseSchema])
def list_agendamentos():
    return get_agendamento_list()

@router.post("/agendamentos/", response_model=AgendamentoResponseSchema, status_code=201)
def create_agendamento(data: AgendamentoRequestSchema):
    return post_agendamento_item(data)

@router.get("/agendamentos/{agendamento_id}", response_model=AgendamentoResponseSchema)
def get_agendamento(agendamento_id: int = Path(..., gt=0)):
    return get_agendamento_item(agendamento_id)

@router.get("/agendamentos/veiculo/{veiculo_id}", response_model=List[AgendamentoResponseSchema])
def list_agendamentos_by_veiculo(veiculo_id: int = Path(..., gt=0)):
    return get_agendamento_by_veiculo_id(veiculo_id)

@router.get("/agendamentos/cliente/{cliente_id}", response_model=List[AgendamentoResponseSchema])
def list_agendamentos_by_cliente(cliente_id: int = Path(..., gt=0)):
    return get_agendamento_by_cliente_id(cliente_id)

@router.put("/agendamentos/{agendamento_id}", response_model=AgendamentoResponseSchema, status_code=201)
def update_agendamento(agendamento_id: int, data: AgendamentoRequestSchema):
    return put_agendamento_item(agendamento_id, data)

@router.delete("/agendamentos/{agendamento_id}", response_model=AgendamentoResponseSchema)
def delete_agendamento(agendamento_id: int = Path(..., gt=0)):
    return delete_agendamento_item(agendamento_id)

@router.put("/agendamentos/{agendamento_id}/concluir", response_model=AgendamentoResponseSchema)
def concluir_agendamento_endpoint(agendamento_id: int, quilometragem_devolucao: int):
    return concluir_agendamento_item(agendamento_id, quilometragem_devolucao)

# ==============================
# ENDPOINTS DOCUMENTO VEICULOS
# ==============================

@router.get("/documentosveiculo/", response_model=List[DocumentoveiculoResponseSchema])
def list_documentosveiculo():
    return get_documentoveiculo_list()

@router.post("/documentosveiculo/", response_model=DocumentoveiculoResponseSchema, status_code=201)
def create_documentoveiculo(data: DocumentoveiculoRequestSchema):
    return post_documentoveiculo_item(data)

@router.get("/documentosveiculo/{documentoveiculo_id}", response_model=DocumentoveiculoResponseSchema)
def get_documentoveiculo(documentoveiculo_id: int = Path(..., gt=0)):
    return get_documentoveiculo_item(documentoveiculo_id)

@router.get("/documentosveiculo/veiculo/{veiculo_id}", response_model=List[DocumentoveiculoResponseSchema])
def list_documentosveiculo_by_veiculo(veiculo_id: int = Path(..., gt=0)):
    return get_documentoveiculo_by_veiculo_id(veiculo_id)

@router.put("/documentosveiculo/{documentoveiculo_id}", response_model=DocumentoveiculoResponseSchema, status_code=201)
def update_documentoveiculo(documentoveiculo_id: int, data: DocumentoveiculoRequestSchema):
    return put_documentoveiculo_item(documentoveiculo_id, data)

@router.delete("/documentosveiculo/{documentoveiculo_id}", response_model=DocumentoveiculoResponseSchema)
def delete_documentoveiculo(documentoveiculo_id: int = Path(..., gt=0)):
    return delete_documentoveiculo_item(documentoveiculo_id)

# ==============================
# ENDPOINTS MANUTENÇÃO
# ==============================

@router.get("/manutencao/", response_model=List[ManutencaoResponseSchema])
def list_manutencoes():
    return get_manutencao_list()

@router.post("/manutencao/", response_model=ManutencaoResponseSchema, status_code=201)
def create_manutencao(data: ManutencaoRequestSchema):
    return post_manutencao_item(data)

@router.get("/manutencao/{manutencao_id}", response_model=ManutencaoResponseSchema)
def get_manutencao(manutencao_id: int = Path(..., gt=0)):
    return get_manutencao_item(manutencao_id)

@router.get("/manutencao/veiculo/{veiculo_id}", response_model=List[ManutencaoResponseSchema])
def list_manutencoes_by_veiculo(veiculo_id: int = Path(..., gt=0)):
    return get_manutencao_by_veiculo_id(veiculo_id)

@router.put("/manutencao/{manutencao_id}", response_model=ManutencaoResponseSchema, status_code=201)
def update_manutencao(manutencao_id: int, data: ManutencaoRequestSchema):
    return put_manutencao_item(manutencao_id, data)

@router.delete("/manutencao/{manutencao_id}", response_model=ManutencaoResponseSchema)
def delete_manutencao(manutencao_id: int = Path(..., gt=0)):
    return delete_manutencao_item(manutencao_id)


# ==============================
# Inicializar no app
# ==============================

def initialize_endpoints(app):
    app.include_router(router)
