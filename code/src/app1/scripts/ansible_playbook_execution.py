import sys
import time
import random
import re

sys.stdout.reconfigure(encoding='utf-8') 
#  Define issue categories & possible reasons
server_issue_mapping = {
    "down": [
        ("Server disk is full", "Calling Ansible Playbook for Freeing up disk space..."),
        ("Critical system service crashed", "Calling Ansible Playbook for Restarting services..."),
        ("Power failure detected", "Calling Ansible Playbook for Rebooting server..."),
        ("Kernel panic occurred", "Calling Ansible Playbook for Running kernel diagnostics..."),
        ("Overheating issue", "Calling Ansible Playbook for Throttling CPU & optimizing cooling..."),
        ("File system corruption", "Calling Ansible Playbook for Performing file system check..."),
    ],
    "unresponsive": [
        ("Memory leak detected", "Calling Ansible Playbook for Restarting affected services..."),
        ("High CPU usage", "Calling Ansible Playbook for Optimizing processes..."),
        ("Database connection timeout", "Calling Ansible Playbook for Resetting DB connections..."),
        ("I/O operations stuck", "Calling Ansible Playbook for Clearing pending operations..."),
        ("Network latency detected", "Calling Ansible Playbook for Adjusting network configurations..."),
        ("Swap memory overload", "Calling Ansible Playbook for Optimizing swap usage..."),
        ("Unauthorized login attempts", "Calling Ansible Playbook for Blocking suspicious IPs..."),
        ("Security patch pending", "Calling Ansible Playbook for Applying latest security updates..."),
    ],
    "slow": [
        ("Excessive disk reads/writes", "Calling Ansible Playbook for Optimizing disk I/O..."),
        ("High RAM usage", "Calling Ansible Playbook for Clearing cache..."),
        ("Multiple long-running queries", "Calling Ansible Playbook for Killing stuck processes..."),
        ("Network congestion", "Calling Ansible Playbook for Reconfiguring network..."),
        ("Service misconfiguration", "Calling Ansible Playbook for Reapplying configuration settings..."),
    ],
}

#  Issue type keywords for extraction
issue_keywords = {
    "down": ["down", "crashed", "not responding", "failure", "stopped", "unavailable"],
    "unresponsive": ["unresponsive", "not working", "timeout", "stuck", "hanged", "halted"],
    "slow": ["slow", "lagging", "delayed", "high load", "sluggish", "performance issue"],
}

def extract_issue_type(query):
    """Extracts the issue type from a given query using predefined keywords."""
    query_lower = query.lower()
    for issue_type, keywords in issue_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            return issue_type
    return None  # Return None if no match is found

def extract_server_name(query):
    """Extracts server name from a query using regex patterns."""
    server_patterns = [
        r"server\s+['\"]?([\w\d-]+)['\"]?",  # Matches: server 'web-server-01'
        r"hostname\s+['\"]?([\w\d-]+)['\"]?",  # Matches: hostname "dbserver02"
        r'server\s+name\s+([\w\d\-_]+)',              # e.g., server name India1234
        r'server\s*["\']?([\w\d\-_]+)["\']?',        # e.g., server: "abhi1234"
        r'ansible\s*[:\-]\s*["\']?([\w\d\-_]+)["\']?',# e.g., grafana: abhi1234
        r'hostname\s*[:\-]?\s*["\']?([\w\d\-_]+)["\']?', # e.g., hostname: abhi1234
        r'ci\s*[:\-]?\s*["\']?([\w\d\-_]+)["\']?' 
    ]
    for pattern in server_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1)  # Extract server name
    return None

def execute_ansible_playbook(server_name, issue_type):
    """Simulate Ansible playbook execution for different server issues."""
    if not server_name:
        print("\n **Error:** Server name not found in query.")
        return

    if not issue_type:
        print("\n **Error:** Could not determine issue type from query.")
        return

    #  Get a random issue & fix from the mapped issue type
    issue, fix_action = random.choice(server_issue_mapping.get(issue_type, [("Unknown issue detected", "Calling Ansible Playbook...")]))

    #  Simulate response with delays
    print(f"\n **Issue detected on {server_name}:** {issue}")
    time.sleep(2)
    print(f"\n**Action:** {fix_action}")
    time.sleep(5)
    #print(f"\n **{server_name} issue resolved successfully!**")

def main():
    """Test different queries without command-line arguments."""
     #  Extract server name & issue type dynamically
    server_name = sys.argv[1]
    issue_type = sys.argv[2]
     #  Execute Ansible playbook simulation
    execute_ansible_playbook(server_name, issue_type)

    # test_queries = [
    #     "Fix issue for server 'web-server-01' because it is down",
    #     "Server dbserver02 is unresponsive, take action",
    #     "Troubleshoot slow response on app-server-03",
    #     "Server test-server-05 is not responding",
    #     "Fix performance issue on server 'app-db-01'",
    #     "Database server 'db-primary' is running slow, investigate"
    # ]

    # for query in test_queries:
    #     print("\n=============================")
    #     print(f"**Processing Query:** {query}")
    #     print("=============================")
        

if __name__ == "__main__":
    main()
