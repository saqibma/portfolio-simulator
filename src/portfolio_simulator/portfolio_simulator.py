import csv
import os
from typing import List, Optional

from src.portfolio_simulator.asset import Asset


class PortfolioSimulator:
    def __init__(self):
        self.portfolios: List[Asset] = []

    def load_portfolios(self, portfolio_file: str) -> None:
        with open(portfolio_file, "r") as file:
            reader = csv.reader(file)
            current_portfolio = None
            for row in reader:
                if row[0] == "NAME":
                    continue
                elif row[0] and row[1]:
                    if current_portfolio:
                        for portfolio in self.portfolios:
                            if portfolio.name == row[0]:
                                portfolio.no_of_shares = float(row[1])
                                current_portfolio.children.append(portfolio)
                                portfolio.parent = current_portfolio
                                self.portfolios.remove(portfolio)
                                break
                        else:
                            child_portfolio = Asset(row[0], float(row[1]))
                            current_portfolio.children.append(child_portfolio)
                            child_portfolio.parent = current_portfolio
                elif row[0] and not row[1]:
                    current_portfolio = Asset(row[0])
                    self.portfolios.append(current_portfolio)

    def traverse_portfolios(self, assets: Optional[List[Asset]] = None) -> None:
        if assets is None:
            assets = self.portfolios
        for asset in assets:
            print(asset)
            self.traverse_portfolios(asset.children)

    def calculate_portfolio_prices(self, prices_file: str, output_file: str) -> None:
        with open(output_file, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["NAME", "PRICE"])
            for chunk in self.stream_csv_in_chunks(prices_file, chunk_size=1):
                calculated_prices = []
                for row in chunk:
                    stock_name, stock_price = row[0], float(row[1])
                    writer.writerow([stock_name, stock_price])
                    self.update_asset_price(
                        self.portfolios, stock_name, stock_price, calculated_prices
                    )
                writer.writerows(calculated_prices)

    def update_asset_price(
        self,
        assets: List[Asset],
        stock_name: str,
        stock_price: float,
        calculated_prices: List[List],
    ) -> None:
        for asset in assets:
            if asset.name == stock_name:
                diff = (stock_price - asset.price) * asset.no_of_shares
                asset.price = stock_price
                while asset.parent:
                    asset = asset.parent
                    if asset.price != 0.0:
                        asset.price += diff
                        calculated_prices.append([asset.name, asset.price])
                    elif asset.has_valid_prices():
                        asset.price = asset.calculate_portfolio_value()
                        calculated_prices.append([asset.name, asset.price])
                return
            self.update_asset_price(
                asset.children, stock_name, stock_price, calculated_prices
            )

    @staticmethod
    def stream_csv_in_chunks(filename: str, chunk_size: int = 10):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            # Skip header if present
            next(reader, None)
            chunk = []
            for row in reader:
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
        if chunk:  # Yield any remaining records
            yield chunk


def main():
    portfolios_csv_path = os.path.join("..", "..", "data", "input", "portfolios.csv")
    prices_csv_path = os.path.join("..", "..", "data", "input", "prices.csv")
    portfolio_prices_csv_path = os.path.join(
        "..", "..", "data", "output", "portfolio_prices.csv"
    )
    simulator = PortfolioSimulator()
    simulator.load_portfolios(portfolios_csv_path)
    simulator.traverse_portfolios()
    simulator.calculate_portfolio_prices(prices_csv_path, portfolio_prices_csv_path)
    print("********************************")
    simulator.traverse_portfolios()


if __name__ == "__main__":
    main()
