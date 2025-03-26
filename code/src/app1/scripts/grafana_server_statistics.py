import sys
import random

def fetch_dummy_grafana_data(server_name):
    # Dummy data for testing
    data = {
        "server": server_name,
        "memory_usage": random.randint(30, 90),
        "disk_usage": random.randint(30, 90)
    }
    return data

def format_data(data):
    # Create a nicely formatted string (using Markdown for bold labels)
    formatted = (
        #"Please see below server details:\n\n"
        f"Please see below details of Server {data['server']}\n"
        f"**Memory Usage:** {data['memory_usage']}%\n"
        f"**Disk Usage:** {data['disk_usage']}%"
    )
    return formatted

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python grafana_server_statistics.py <server_name>")
    else:
        server_name = sys.argv[1]
        data = fetch_dummy_grafana_data(server_name)
        formatted_output = format_data(data)
        print(formatted_output)
