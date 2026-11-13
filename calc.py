"""Portfolio math. Plain functions, no Flask and no internet, so they're easy to test."""


def gain_loss(quantity, buy_price, current_price):
    """Return (value, gain, gain_pct) for one holding."""
    cost = quantity * buy_price
    value = quantity * current_price
    gain = value - cost
    gain_pct = gain / cost * 100 if cost > 0 else 0.0
    return value, gain, gain_pct


def sort_by_value(holdings):
    """Sort holdings (list of dicts) from highest value to lowest."""
    return sorted(holdings, key=lambda h: h["value"], reverse=True)


def best_performer(holdings):
    """Return the holding with the highest gain_pct, or None if the list is empty."""
    best = None
    for h in holdings:
        if best is None or h["gain_pct"] > best["gain_pct"]:
            best = h
    return best
