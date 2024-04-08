import os
import pytest
from src.portfolio_simulator.portfolio_simulator import PortfolioSimulator
from src.portfolio_simulator.asset import Asset


@pytest.fixture
def portfolios_csv_path():
    return os.path.join("data", "input", "portfolios.csv")


@pytest.fixture
def prices_csv_path():
    return os.path.join("data", "input", "prices.csv")


@pytest.fixture
def portfolio_prices_csv_path():
    return os.path.join("data", "output", "portfolio_prices.csv")


def test_load_portfolios(portfolios_csv_path):
    simulator = PortfolioSimulator()
    simulator.load_portfolios(portfolios_csv_path)
    assert len(simulator.portfolios) == 1


def test_calculate_portfolio_prices(
    portfolios_csv_path, prices_csv_path, portfolio_prices_csv_path
):
    simulator = PortfolioSimulator()
    simulator.load_portfolios(portfolios_csv_path)
    simulator.calculate_portfolio_prices(prices_csv_path, portfolio_prices_csv_path)
    assert os.path.exists(portfolio_prices_csv_path)


def test_update_asset_price():
    simulator = PortfolioSimulator()
    asset1 = Asset("Asset1", 100, 10.0)
    asset2 = Asset("Asset2", 200, 20.0)
    asset3 = Asset("Asset3", 300, 0.0)
    simulator.portfolios = [asset1, asset2, asset3]
    calculated_prices = []
    simulator.update_asset_price(
        simulator.portfolios, "Asset1", 15.0, calculated_prices
    )
    assert asset1.price == 15.0
    assert asset2.price == 20.0
    assert asset3.price == 0.0


if __name__ == "__main__":
    pytest.main([__file__])
