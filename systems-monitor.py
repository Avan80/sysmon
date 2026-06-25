import psutil

cpu_percent = psutil.cpu_percent(interval=1)
cpu_threads = psutil.cpu_count()
load_average = psutil.getloadavg()

free_mem = psutil.virtual_memory().percent
available_mem = psutil.virtual_memory().available

io_stats = psutil.net_io_counters()

print("CPU")

print(f"  {'CPU usage percentage':<20} = {cpu_percent}%")
print(f"  {'CPU threads':<20} = {cpu_threads}")
print(f"  {'Load average':<20} = 1m {load_average[0]} / 5m {load_average[1]} / 15m {load_average[2]}")

print("Memory")

print(f"  {'Free':<20} = {free_mem}%")
print(f"  {'Available':<20} = {available_mem / 1024**3:.2f} GB")

print("Disk")

for partition in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"  {partition.mountpoint:<20} = {usage.percent}%")
    except PermissionError:
        pass

print("Network")

print(f"  {'Bytes sent':<20} = {io_stats.bytes_sent / 1024**2:.2f} MB")
print(f"  {'Bytes received':<20} = {io_stats.bytes_recv / 1024**2:.2f} MB")
print(f"  {'Packets sent':<20} = {io_stats.packets_sent}")
print(f"  {'Packets received':<20} = {io_stats.packets_recv}")
