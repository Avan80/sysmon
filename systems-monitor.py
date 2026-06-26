import psutil
import json

cpu_percent = psutil.cpu_percent(interval=1)
cpu_threads = psutil.cpu_count()
load_average = psutil.getloadavg()
free_mem = psutil.virtual_memory().percent
available_mem = psutil.virtual_memory().available
io_stats = psutil.net_io_counters()

disk = {}
for partition in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        disk[partition.mountpoint] = usage.percent
    except PermissionError:
        pass

metrics = {
    "CPU": {
        "CPU usage percentage": cpu_percent,
        "CPU threads": cpu_threads,
        "Load average": load_average,
    },
    "Memory": {
        "Free": free_mem,
        "Available": round(available_mem / 1024**3, 2),
    },
    "Disk": disk,
    "Network": {
        "Bytes sent": round(io_stats.bytes_sent / 1024**2, 2),
        "Bytes received": round(io_stats.bytes_recv / 1024**2, 2),
        "Packets sent": io_stats.packets_sent,
        "Packets received": io_stats.packets_recv,
    }
}

print(json.dumps(metrics, indent=2))
