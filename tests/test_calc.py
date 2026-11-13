from calc import best_performer, gain_loss, sort_by_value


def test_gain():
    value, gain, pct = gain_loss(2, 100, 150)
    assert (value, gain, pct) == (300, 100, 50)


def test_loss():
    value, gain, pct = gain_loss(1, 100, 80)
    assert gain == -20 and pct == -20


def test_zero_cost_does_not_crash():
    assert gain_loss(1, 0, 50)[2] == 0.0


def test_sort_by_value_highest_first():
    data = [{"value": 5}, {"value": 50}, {"value": 20}]
    assert [h["value"] for h in sort_by_value(data)] == [50, 20, 5]


def test_best_performer():
    data = [{"symbol": "A", "gain_pct": 5}, {"symbol": "B", "gain_pct": 12}, {"symbol": "C", "gain_pct": -3}]
    assert best_performer(data)["symbol"] == "B"


def test_best_performer_empty():
    assert best_performer([]) is None
