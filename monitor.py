import psutil
import time
import os

def check_log_size(log_file_path, max_size=500*1024*1024): # 500 МБ
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) >= max_size:
        new_log_file = log_file_path.replace(".txt", f"_{time.strftime('%Y%m%d%H%M%S')}.txt")
        os.rename(log_file_path, new_log_file)

def get_cpu_times():
    cpu_times = psutil.cpu_times_percent(interval=1)
    return {
        "user": cpu_times.user,
        "system": cpu_times.system,
        "nice": cpu_times.nice,
        "idle": cpu_times.idle,
        "iowait": cpu_times.iowait,
        "irq": cpu_times.irq,
        "softirq": cpu_times.softirq,
        "steal": cpu_times.steal
    }

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.used / memory.total * 100

def get_disk_usage(disk_path="/"):
    disk_usage = psutil.disk_usage(disk_path)
    return disk_usage.used / disk_usage.total * 100

def get_system_load():
    return os.getloadavg()

def get_network_info():
    net_io = psutil.net_io_counters()
    return f"Sent: {net_io.bytes_sent} bytes, Received: {net_io.bytes_recv} bytes"

def log_data(log_file_path="system_monitor_log.txt"):
    check_log_size(log_file_path)
    cpu_times = get_cpu_times()
    with open(log_file_path, "a") as log_file:
        log_file.write(f"CPU Usage - User: {cpu_times['user']}%, System: {cpu_times['system']}%, Nice: {cpu_times['nice']}%, Idle: {cpu_times['idle']}%, IOWait: {cpu_times['iowait']}%, IRQ: {cpu_times['irq']}%, SoftIRQ: {cpu_times['softirq']}%, Steal: {cpu_times['steal']}%\n")
        log_file.write(f"Memory Usage: {get_memory_usage()}%\n")
        log_file.write(f"Disk Usage: {get_disk_usage()}%\n")
        log_file.write(f"System Load (1, 5, 15 min): {get_system_load()}\n")
        log_file.write(f"Network Info: {get_network_info()}\n")
        log_file.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("----------------------------\n")

def main():
    while True:
        log_data()
        time.sleep(60)  # Снимает метрики каждые 60 секунд

if __name__ == "__main__":
    main()
