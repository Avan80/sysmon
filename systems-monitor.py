import psutil
import json
import os
import time
from datetime import datetime, timezone

os.makedirs("/var/log/sysmon", exist_ok=True)
while True:
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_threads = psutil.cpu_count()
    cpu_frequency = psutil.cpu_freq()
    cpu_times = psutil.cpu_times()
    load_average = psutil.getloadavg()
    free_mem = psutil.virtual_memory().percent
    available_mem = psutil.virtual_memory().available
    swap_mem = psutil.virtual_memory().swap
    io_stats = psutil.net_io_counters()
    tcp_connections = len(psutil.net_connections(kind='tcp'))
    udp_connections = len(psutil.net_connections(kind='udp'))
    disk = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk[partition.mountpoint] = usage.percent
        except PermissionError:
            pass

    metrics = {
        "Time": datetime.now(timezone.utc).isoformat(),
        "CPU": {
            "CPU usage percentage": cpu_percent,
            "CPU threads": cpu_threads,
            "Load average": load_average,
            "CPU frequency": cpu_frequency,
            "CPU times": cpu_times,
        },
        "Memory": {
            "Free": free_mem,
            "Available": round(available_mem / 1024**3, 2),
            "Swap": round(swap_mem / 1024**3, 2),
        },
        "Disk": disk,
        "Network": {
            "Bytes sent": round(io_stats.bytes_sent / 1024**2, 2),
            "Bytes received": round(io_stats.bytes_recv / 1024**2, 2),
            "Packets sent": io_stats.packets_sent,
            "Packets received": io_stats.packets_recv,
            "TCP connection count": tcp_connections,
            "UDP connection count": udp_connections,
        }
    }

    with open("/var/log/sysmon/metrics.log", "a") as file:
        file.write(json.dumps(metrics) + "\n")
    time.sleep(30)
