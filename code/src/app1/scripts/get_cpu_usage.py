import psutil

# Get the CPU usage percentage over a 1-second interval
cpu_usage = psutil.cpu_percent(interval=1)
print(f"CPU Usage: {cpu_usage}%")
