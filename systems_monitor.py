import psutil
import json
import os
import time
from datetime import datetime, timezone
import logging

os.makedirs("/var/log/sysmon", exist_ok=True)

logging.basicConfig(
    filename="/var/log/sysmon/sysmon.log",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s"
)

def metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_threads = psutil.cpu_count()
    cpu_frequency = psutil.cpu_freq()
    cpu_times = psutil.cpu_times()
    load_average = psutil.getloadavg()
    free_mem = psutil.virtual_memory().percent
    available_mem = psutil.virtual_memory().available
    swap_mem = psutil.swap_memory().percent
    io_stats = psutil.net_io_counters()
    tcp_connections = len(psutil.net_connections(kind='tcp'))
    udp_connections = len(psutil.net_connections(kind='udp'))
    net_errors_in = io_stats.errin
    net_drops_in = io_stats.dropin
    disk = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk[partition.mountpoint] = usage.percent
        except PermissionError:
            logging.warning(f"permission denied: {partition.mountpoint}")

    return {
        "Time": datetime.now(timezone.utc).isoformat(),
        "CPU": {
            "CPU usage percentage": cpu_percent,
            "CPU threads": cpu_threads,
            "Load average": load_average,
            "CPU frequency": cpu_frequency.current,
            "CPU user time": cpu_times.user,
            "CPU system time": cpu_times.system,
            "CPU idle time": cpu_times.idle,
        },
        "Memory": {
            "Used": free_mem,
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
            "Network errors": net_errors_in,
            "Network drops": net_drops_in, 
        }
    }
def run():
    while True:
        metric = metrics()
        with open("/var/log/sysmon/metrics.log", "a") as file:
            file.write(json.dumps(metric) + "\n")
        if metric["CPU"]["CPU usage percentage"] > 80:
            logging.warning(f"CPU usage high: {metric['CPU']['CPU usage percentage']}%")
        if metric["Memory"]["Used"] > 90:
            logging.warning(f"Memory usage high: {metric['Memory']['Used']}%")
        if metric["Memory"]["Swap"] > 35:
            logging.warning(f"Memory constrained, swap usage high: {metric['Memory']['Swap']}%")
        for mountpoint, percent in metric["Disk"].items():
            if percent > 80:
                logging.warning(f"Disk usage high on {mountpoint}: {percent}%") 
        if metric["Network"]["Network errors"] > 0:
            logging.warning(f"Network errors incoming: {metric['Network']['Network errors']}")
        if metric["Network"]["Network drops"] > 0:
            logging.warning(f"Network drops incoming: {metric['Network']['Network drops']}")
        time.sleep(30)

if __name__ == "__main__":
    run()
