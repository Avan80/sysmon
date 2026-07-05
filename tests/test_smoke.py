import systems_monitor
import logging

def test_import():
    assert systems_monitor is not None

def test_metric_values():
    results = systems_monitor.metrics()
    assert results["CPU"]["CPU usage percentage"] >= 0
    assert results["CPU"]["CPU usage percentage"] <= 100
    assert results["CPU"]["CPU threads"] > 0
    assert results["CPU"]["CPU frequency"] > 0
    assert results["Memory"]["Used"] >= 0
    assert results["Memory"]["Swap"] >= 0
    for mountpoint, percent in results["Disk"].items():
        assert percent >= 0
        assert percent <= 100
    assert results["Network"]["Bytes sent"] >= 0
    assert results["Network"]["Bytes received"] >= 0
    assert results["Network"]["Packets sent"] >= 0
    assert results["Network"]["Packets received"] >= 0
    assert results["Network"]["Network errors"] >= 0
    assert results["Network"]["Network drops"] >= 0

def test_check_thresholds(caplog):
        f_metric = {
            "CPU": {"CPU usage percentage": 81},
            "Memory": {"Used": 10, "Swap": 5},
            "Disk": {},
            "Network": {"Network errors": 0, "Network drops": 0}
        }

        with caplog.at_level(logging.WARNING):
            systems_monitor.check_thresholds(f_metric)
            assert "CPU usage high" in caplog.text
