from typing import List, Optional


class Asset:
    def __init__(self, name: str, no_of_shares: int = 1, price: float = 0.0):
        self.name = name
        self.no_of_shares = no_of_shares  # no_of_assets
        self.children: List[Asset] = []
        self.price = price
        self.parent: Optional[Asset] = None

    def has_valid_prices(self) -> bool:
        """
        Check if all asset prices are non-zero
        """
        return len(self.children) > 0 and all(
            asset.price != 0.0 for asset in self.children
        )

    def calculate_portfolio_value(self) -> float:
        """
        Calculate the total value of the portfolio by summing
        the product of price and number of shares for each asset
        """
        return sum(asset.price * asset.no_of_shares for asset in self.children)

    def __repr__(self) -> str:
        return (
            f"Asset(name='{self.name}', "
            f"no_of_shares={self.no_of_shares}, "
            f"price={self.price}, "
            f"children={self.children})"
        )
