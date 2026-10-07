from abc import ABC, abstractmethod


class Product:
    def __init__(self, name: str, price: float) -> None:
        if not name.strip():
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Product price cannot be negative.")

        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"


class DiscountStrategy(ABC):

    @abstractmethod
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        pass

    @abstractmethod
    def apply_discount(self, product: Product) -> float:
        pass


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percent: int) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Discount percentage must be between 0 and 100.")

        self.percent = percent

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return self.percent <= 70

    def apply_discount(self, product: Product) -> float:
        return product.price * (1 - self.percent / 100)


class FixedAmountDiscount(DiscountStrategy):

    def __init__(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")

        self.amount = amount

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return product.price * 0.9 > self.amount

    def apply_discount(self, product: Product) -> float:
        return max(0, product.price - self.amount)


class PremiumUserDiscount(DiscountStrategy):

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return user_tier.strip().lower() == "premium"

    def apply_discount(self, product: Product) -> float:
        return product.price * 0.80


class DiscountEngine:

    def __init__(self, strategies: list[DiscountStrategy]) -> None:
        self.strategies = strategies

    def calculate_best_price(
        self,
        product: Product,
        user_tier: str
    ) -> float:

        prices = [product.price]

        for strategy in self.strategies:
            if strategy.is_applicable(product, user_tier):
                discounted_price = strategy.apply_discount(product)
                prices.append(discounted_price)

        return min(prices)


def main() -> None:

    product = Product("Wireless Mouse", 50.00)
    user_tier = "Premium"

    strategies = [
        PercentageDiscount(10),
        FixedAmountDiscount(5),
        PremiumUserDiscount()
    ]

    discount_engine = DiscountEngine(strategies)

    best_price = discount_engine.calculate_best_price(
        product,
        user_tier
    )

    print("=" * 40)
    print("        DISCOUNT CALCULATOR")
    print("=" * 40)
    print(f"Product       : {product.name}")
    print(f"Original Price: ${product.price:.2f}")
    print(f"User Tier     : {user_tier}")
    print(f"Best Price    : ${best_price:.2f}")
    print("=" * 40)


if __name__ == "__main__":
    main()