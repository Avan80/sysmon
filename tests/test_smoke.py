import systems_monitor

def test_import():
    assert systems_monitor is not None

def test_metric_keys():
    results = systems_monitor.metrics()
    assert "CPU" in results
    assert "Memory" in results
    assert "Disk" in results