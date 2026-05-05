Atividade Realizada no dia 04/05/2026 na aula Desenvolvimento Rápido de Aplicações em Python. 
Esse exercicio é sobre pyteste e fastapi. 
Na atividade o pytest foi adicionado sobre cancelar pedido e listar os cancelamento pedidos. 
O foco da atividade foi a implementação de uma lógica segura de cancelamento de pedidos e a rastreabilidade dessas operações através de listagens específicas.
Novidade desta versão são: Cancelamento de Pedidos, Listagem de Cancelamentos e Testes no Pytest.

TESTES PYTEST: 
Foram adicionados testes de cobertura para o cancelamento de pedidos.
1- Garante que o status do pedido muda corretamente: `test_cancelar_pedido_sucesso`
2- Valida se a lista retorna apenas os itens cancelados: `test_listar_pedidos_cancelados`
3- Impede que um pedido já entregue seja cancelado: `test_erro_cancelar_pedido_finalizado`

COMO RODAR O PROJETO: 
Os comandos para ativar e como rodar o pyteste.
1- Para rodar os testes, utilize: pytest -v tests/test_pedidos.py
2- Ative seu ambiente virtual: .\venv\Scripts\activate
3- Instale as dependências: pip install -r requirements.txt
4- Inicie a API: uvicorn main:app --reload
5- Rodar os Testes de Cancelamento: pytest
6- Executar: uvicorn main:app --reload
