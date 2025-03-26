import psutil

# Get the system's memory usage percentage
memory_usage = psutil.virtual_memory().percent
print(f"Memory Usage: {memory_usage}%")