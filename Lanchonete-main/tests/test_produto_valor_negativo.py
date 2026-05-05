import pytest
from domain.produto import Produto
def test_produto_valor_negativo():
        with pytest.raises(ValueError):
            Produto(codigo=1, valor=-5, tipo=1)