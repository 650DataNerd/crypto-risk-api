from decimal import Decimal
from app.services.risk_service import (
    compute_returns,
    compute_volatility,
    compute_max_drawdown,
)


def test_compute_returns_basic():
    prices = [Decimal("100"), Decimal("110"), Decimal("99")]
    returns = compute_returns(prices)
    assert len(returns) == 2
    assert returns[0] == Decimal("0.1")


def test_compute_returns_empty():
    assert compute_returns([]) == []
    assert compute_returns([Decimal("100")]) == []


def test_compute_volatility_returns_none_for_insufficient_data():
    assert compute_volatility([Decimal("100")]) is None
    assert compute_volatility([]) is None


def test_compute_volatility_stable_prices():
    prices = [Decimal("100")] * 10
    volatility = compute_volatility(prices)
    assert volatility == Decimal("0")


def test_compute_max_drawdown_basic():
    prices = [
        Decimal("60000"),
        Decimal("70000"),
        Decimal("64000"),
    ]
    drawdown = compute_max_drawdown(prices)
    assert drawdown is not None
    assert drawdown < Decimal("0")


def test_compute_max_drawdown_no_drawdown():
    prices = [Decimal("100"), Decimal("110"), Decimal("120")]
    drawdown = compute_max_drawdown(prices)
    assert drawdown == Decimal("0")


def test_compute_max_drawdown_insufficient_data():
    assert compute_max_drawdown([Decimal("100")]) is None
    assert compute_max_drawdown([]) is None
