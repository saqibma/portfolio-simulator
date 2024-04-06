class Asset:
    def __init__(self, name, no_of_shares=1, price=0.0):
        self.name = name
        self.no_of_shares = no_of_shares
        self.children = []
        self.price = price
        self.process = False
        self.parent = None

    def has_valid_prices(self):
        """
        Check if all asset prices are non-zero
        """
        return (
            self.process
            and len(self.children) > 0
            and all(asset.price != 0.0 for asset in self.children)
        )

    def calculate_portfolio_value(self):
        """
        Calculate the total value of the portfolio by summing
        the product of price and number of shares for each asset
        """
        return sum(
            map(lambda asset: asset.price * asset.no_of_shares, self.children)
        )

    def __repr__(self):
        return (
            f"Asset(name='{self.name}', "
            f"no_of_shares={self.no_of_shares}, "
            f"price={self.price}, "
            f"process={self.process}, "
            f"children={self.children})"
        )
