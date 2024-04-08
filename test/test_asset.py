import pytest
from src.portfolio_simulator.asset import Asset


@pytest.fixture
def asset_with_non_zero_prices():
    asset = Asset("TECH", 100)
    asset.children = [
        Asset("AAPL", 10, price=150.0),
        Asset("MSFT", 20, price=100.0),
        Asset("NVDA", 15, price=200.0),
    ]
    return asset


@pytest.fixture
def asset_with_zero_prices():
    asset = Asset("AUTOS", 100)
    asset.children = [
        Asset("FORD", 10, price=0.0),
        Asset("TSLA", 20, price=0.0),
        Asset("BMW", 15, price=0.0),
    ]
    return asset


@pytest.fixture
def asset_with_no_children():
    asset = Asset("COMMODITY")
    return asset


def test_has_valid_prices_all_assets_non_zero(asset_with_non_zero_prices):
    assert asset_with_non_zero_prices.has_valid_prices()


def test_has_valid_prices_some_assets_zero(asset_with_zero_prices):
    assert not asset_with_zero_prices.has_valid_prices()


def test_has_valid_prices_no_children(asset_with_no_children):
    assert not asset_with_no_children.has_valid_prices()


def test_calculate_portfolio(asset_with_non_zero_prices):
    assert asset_with_non_zero_prices.calculate_portfolio_value() == 6500


def test_repr(asset_with_non_zero_prices):
    assert (
        repr(asset_with_non_zero_prices)
        == "Asset(name='TECH', no_of_shares=100, price=0.0, children=["
        "Asset(name='AAPL', no_of_shares=10, price=150.0, children=[]), "
        "Asset(name='MSFT', no_of_shares=20, price=100.0, children=[]), "
        "Asset(name='NVDA', no_of_shares=15, price=200.0, children=[])"
        "])"
    )

if __name__ == "__main__":
    pytest.main([__file__])
