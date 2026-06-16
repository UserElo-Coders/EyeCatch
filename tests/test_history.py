from core.history import HistoryManager


def test_history_limit():
    history = HistoryManager(maxlen=3)

    history.update(10, 20, 30, 40)
    history.update(11, 21, 31, 41)
    history.update(12, 22, 32, 42)
    history.update(13, 23, 33, 43)

    assert history.get("cpu_usage") == [11, 12, 13]


def test_empty_series():
    history = HistoryManager()

    assert history.get("cpu_usage") == []


def test_invalid_series():
    history = HistoryManager()

    assert history.get("invalid_metric") == []