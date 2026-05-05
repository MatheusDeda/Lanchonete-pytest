from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from schemas.pedido import PedidoCreate, PedidoAddItem, PedidoOut
from services.lanchonete_service import service

router = APIRouter(prefix="/lanchonete/pedidos", tags=["pedidos"])

@router.post("", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def criar(payload: PedidoCreate):
    """Cria um pedido com o primeiro produto já adicionado."""
    pedido = service.criar_pedido(payload.cpf, payload.cod_produto, payload.qtd_max_produtos)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente ou produto não encontrado"
        )

    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        esta_cancelado=pedido.esta_cancelado,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )


@router.put("/{cod_pedido}/itens", status_code=status.HTTP_200_OK)
def adicionar_item(cod_pedido: int, payload: PedidoAddItem) -> Dict[str, Any]:
    """Adiciona um produto a um pedido existente."""
    ok = service.alterar_pedido(cod_pedido, payload.cod_produto)
    
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pedido/produto inválido ou limite excedido"
        )
    return {"ok": True, "mensagem": "Item adicionado com sucesso"}


@router.post("/{cod_pedido}/finalizar", status_code=status.HTTP_200_OK)
def finalizar(cod_pedido: int) -> Dict[str, float]:
    """Finaliza um pedido e retorna o total calculado."""
    total = service.finalizar_pedido(cod_pedido)
    
    if total is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido não encontrado ou já finalizado"
        )
    return {"total": total}


@router.get("/cancelados", response_model=list[PedidoOut], status_code=status.HTTP_200_OK)
def listar_pedidos_cancelados():
    """Lista todos os pedidos que foram cancelados."""
    pedidos = service.listar_pedidos_cancelados()
    
    return [
        PedidoOut(
            codigo=pedido.codigo,
            cpf=pedido.cliente.cpf,
            esta_entregue=pedido.esta_entregue,
            esta_cancelado=pedido.esta_cancelado,
            produtos=[p.codigo for p in pedido.listaProdutos]
        )
        for pedido in pedidos
    ]


@router.post("/{cod_pedido}/cancelar", status_code=status.HTTP_200_OK)
def cancelar_pedido(cod_pedido: int) -> Dict[str, Any]:
    """Realiza o cancelamento lógico de um pedido."""
    resultado = service.cancelar_pedido(cod_pedido)

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pedido não encontrado, já entregue ou já cancelado"
        )

    return {"ok": True, "mensagem": "Pedido cancelado com sucesso"}


@router.get("/{cod_pedido}", response_model=PedidoOut, status_code=status.HTTP_200_OK)
def obter(cod_pedido: int):
    """Busca os detalhes de um pedido específico pelo seu código."""
    pedido = service.obter_pedido(cod_pedido)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido não encontrado"
        )
        
    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        esta_cancelado=pedido.esta_cancelado,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )