import systems_monitor

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