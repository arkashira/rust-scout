from src.axentx_product.product import Product
from src.axentx_product.portfolio import Portfolio
from src.axentx_product.chain_playbook import ChainPlaybook

def test_product():
    product = Product("Test Product", 10)
    assert str(product) == "Test Product: 10"

def test_portfolio():
    portfolio = Portfolio()
    product = Product("Test Product", 10)
    portfolio.add_product(product)
    assert len(portfolio.get_products()) == 1

def test_chain_playbook():
    chain_playbook = ChainPlaybook()
    product = Product("Test Product", 10)
    chain_playbook.add_product_to_portfolio(product)
    portfolio = chain_playbook.get_portfolio()
    assert len(portfolio.get_products()) == 1
