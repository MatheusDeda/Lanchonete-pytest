def test_deve_cancelar_pedido_com_sucesso(client):
    # 1. Criar cliente
    client.post("/lanchonete/clientes", json={
        "cpf": "11122233344", 
        "nome": "João da Silva", 
        "email": "joao@email.com"
    })

    # 2. Criar produto
    client.post("/lanchonete/produtos", json={
        "codigo": 1, 
        "nome": "Hambúrguer", 
        "valor": 25.0, 
        "tipo": 1
    })

    # 3. Criar pedido
    res_pedido = client.post("/lanchonete/pedidos", json={
        "cpf": "11122233344", 
        "cod_produto": 1, 
        "qtd_max_produtos": 5
    })
    print("\n--- RESPOSTA DA API ---", res_pedido.json())
    cod_pedido = res_pedido.json()["codigo"]

    # 4. Ação: Cancelar pedido
    response = client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    # Validações
    assert response.status_code == 200
    data = response.json()
    
    # Validar se data["ok"] é True e a mensagem de sucesso
    assert data["ok"] is True
    assert data["mensagem"] == "Pedido cancelado com sucesso"


def test_nao_deve_cancelar_pedido_inexistente(client):
    # Ação: Tentar cancelar um ID que sabidamente não existe
    response = client.post("/lanchonete/pedidos/999999/cancelar")

    # Validar status_code 400 (conforme configurado na sua rota)
    assert response.status_code == 400

    data = response.json()
    
    # Validar mensagem de erro vinda do HTTPException
    assert "detail" in data
    assert "Pedido não encontrado" in data["detail"]


def test_nao_deve_cancelar_pedido_finalizado(client):
    # 1. Setup inicial (Cliente, Produto, Pedido)
    client.post("/lanchonete/clientes", json={"cpf": "55566677788", "nome": "Maria", "email": "maria@email.com"})
    client.post("/lanchonete/produtos", json={"codigo": 2, "nome": "Refrigerante", "valor": 8.0, "tipo": 2})
    
    res_pedido = client.post("/lanchonete/pedidos", json={
        "cpf": "55566677788", 
        "cod_produto": 2, 
        "qtd_max_produtos": 2
    })
    cod_pedido = res_pedido.json()["codigo"]

    # 2. Finalizar pedido
    client.post(f"/lanchonete/pedidos/{cod_pedido}/finalizar")

    # 3. Ação: Tentar cancelar um pedido já finalizado
    response = client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    # Validações de erro
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "não pode ser cancelado" in data["detail"] or "já entregue" in data["detail"]


def test_deve_listar_pedidos_cancelados(client):
    # 1. Setup: Criar recursos
    client.post("/lanchonete/clientes", json={"cpf": "99988877766", "nome": "Pedro", "email": "pedro@email.com"})
    client.post("/lanchonete/produtos", json={"codigo": 3, "nome": "Batata Frita", "valor": 12.0, "tipo": 3})
    
    res_pedido = client.post("/lanchonete/pedidos", json={
        "cpf": "99988877766", 
        "cod_produto": 3, 
        "qtd_max_produtos": 3
    })
    cod_pedido = res_pedido.json()["codigo"]

    # 2. Cancelar o pedido para garantir que ele entre na lista
    client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    # 3. Ação: Listar cancelados
    response = client.get("/lanchonete/pedidos/cancelados")

    assert response.status_code == 200
    data = response.json()

    # Validar se retornou uma lista
    assert isinstance(data, list)

    # Validar se existe pelo menos um pedido cancelado
    assert len(data) > 0

    # Validar se esta_cancelado é True no pedido que acabamos de cancelar
    # Encontra o pedido específico na lista gerada
    pedido_cancelado = next((p for p in data if p["codigo"] == cod_pedido), None)
    
    assert pedido_cancelado is not None, "O pedido cancelado não apareceu na listagem"
    assert pedido_cancelado["esta_cancelado"] is True