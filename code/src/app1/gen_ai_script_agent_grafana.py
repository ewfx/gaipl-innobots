import os
import subprocess
import re

class gen_ai_script_executer:
    """Agent to execute scripts for system monitoring, Grafana queries, and Ansible playbook execution."""

    def __init__(self, scripts_path="./scripts"):
        self.scripts_path = scripts_path

        # ✅ Mapping of keywords to script file names
        self.script_mapping = {
            "cpu usage": "get_cpu_usage.py",
            "memory usage": "get_memory_usage.py",
            "grafana": "grafana_server_statistics.py",
            "ansible": "ansible_playbook_execution.py"  # ✅ Added Ansible execution script
        }

        # ✅ Regex patterns to extract server names correctly
        self.server_name_patterns = [
            r'server\s+name\s+([\w\d]+)',              # e.g., server name India1234
            r'server\s+name\s*["\']([^"\']+)["\']',      # e.g., server name "abhi1234"
            r'grafana\s*[:\-]\s*["\']?([\w\d]+)["\']?',   # e.g., grafana: abhi1234
            r'server\s*[:\-]?\s*["\']?([\w\d]+)["\']?',    # e.g., server: abhi1234 or server abhi1234
            r'hostname\s*[:\-]?\s*["\']?([\w\d]+)["\']?',   # e.g., hostname: abhi1234
            r'ci\s*[:\-]?\s*["\']?([\w\d]+)["\']?'         # e.g., ci: abhi1234
        ]

        # ✅ Keywords for Ansible execution
        self.issue_keywords = {
            "down": ["down", "not responding", "crashed", "unavailable"],
            "unresponsive": ["unresponsive", "frozen", "hanging"],
            "slow": ["slow", "lagging", "delayed", "taking too long"]
        }

    def execute_script(self, query):
        """Determine which script to run based on the query and pass parameters if needed."""
        query_lower = query.lower()
        print(f"Processing query: {query_lower}", flush=True)

        # ✅ Step 1: Check for Ansible Playbook Execution
        if any(keyword in query_lower for keyword in ["ansible", "down", "slow", "unresponsive"]):
            print("In Ansible")
            return self.execute_ansible_script(query_lower)

        # ✅ Step 2: Check for Grafana Execution
        #if "grafana" in query_lower:
        if any(keyword in query_lower for keyword in ["grafana", "monitoring", "telemetry", "statistics","performance","availability"]):
            return self.execute_grafana_script(query_lower)

        # ✅ Step 3: Directly map keyword-based scripts
        for keyword, script in self.script_mapping.items():
            if keyword in query_lower:
                return self.run_script(script)

        return "⚠️ No relevant script found for the query."

    def execute_ansible_script(self, query):
        """Extract server name & issue type and execute Ansible Playbook."""
        server_name = self.extract_server_name(query)
        issue_type = self.extract_issue_type(query)

        if server_name and issue_type:
            print(f"✅ Extracted Server: {server_name}, Issue Type: {issue_type}", flush=True)
            return self.run_ansible_script_with_params(self.script_mapping["ansible"], server_name, issue_type)

        return "⚠️ Could not extract server name or issue type for Ansible Playbook execution."

    def execute_grafana_script(self, query):
        """Extract server name and execute Grafana script."""
        server_name = self.extract_server_name(query)
        if server_name:
            print(f"✅ Extracted Server for Grafana: {server_name}", flush=True)
            return self.run_script_with_param(self.script_mapping["grafana"], server_name)

        return "⚠️ No server name found for Grafana query."

    def extract_server_name(self, query):
        """Extracts the server name from the query using regex patterns."""
        for pattern in self.server_name_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                extracted_name = match.group(1)
                print(f"✅ Server Name Matched: {extracted_name}", flush=True)
                return extracted_name
        print("⚠️ No server name found in query.", flush=True)
        return None

    def extract_issue_type(self, query):
        """Extracts the issue type (down, unresponsive, slow) from the query."""
        for issue, keywords in self.issue_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    print(f"✅ Issue Type Detected: {issue}", flush=True)
                    return issue
        print("⚠️ No issue type detected in query.", flush=True)
        return None

    def run_script(self, script_name):
        """Execute a script without parameters."""
        script_path = os.path.join(self.scripts_path, script_name)
        if not os.path.exists(script_path):
            return f"❌ Error: Script '{script_name}' not found."

        try:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            return result.stdout.strip() if result.stdout else "⚠️ No output generated."
        except Exception as e:
            return f"❌ Error executing script: {str(e)}"

    def run_script_with_param(self, script_name, param):
        """Execute a script with a single parameter (e.g., server name)."""
        script_path = os.path.join(self.scripts_path, script_name)
        print(f"🛠 Running grafana Script")
        print(f"📌 Script Path: {script_path}")
       # print(f"📌 Arguments: Server Name = '{server_name}'", flush=True)        
        
        if not os.path.exists(script_path):
            return f"❌ Error: Script '{script_name}' not found."

        try:
            print(f"🛠 Grafana try 1")
            result = subprocess.run(["python", script_path, param], capture_output=True, text=True)
            return result.stdout.strip() if result.stdout else "⚠️ No output generated."
        except Exception as e:
            return f"❌ Error executing script: {str(e)}"

    def run_ansible_script_with_params(self, script_name, server_name, issue_type):
        """Execute the Ansible script with two parameters (server name & issue type)."""
        script_path = os.path.join(self.scripts_path, script_name)
    
        # ✅ Debugging: Print script path and arguments before execution
        print(f"🛠 Running Ansible Script")
        print(f"📌 Script Path: {script_path}")
        print(f"📌 Arguments: Server Name = '{server_name}', Issue Type = '{issue_type}'", flush=True)
    
        # ✅ Check if the script exists
        if not os.path.exists(script_path):
            print(f"❌ Error: Script '{script_name}' not found at {script_path}")
            return f"❌ Error: Script '{script_name}' not found."
    
        try:
            print(f"📌 Calling try 1 result")  # ✅ Confirm reaching this point
    
            # ✅ Run the subprocess and capture output & errors
            result = subprocess.run(
                ["python", script_path, server_name, issue_type],
                capture_output=True,
                text=True,
                check=True  # ✅ Forces exception if the script fails
            )
    
            print(f"📌 After try result")  # ✅ Check if this prints after execution
    
            # ✅ Print the full output (stdout + stderr)
            if result.stdout:
                print(f"✅ Ansible Execution Output:\n")
            if result.stderr:
                print(f"⚠️ Ansible Execution Error:\n{result.stderr}")
    
            return result.stdout.strip() if result.stdout else "⚠️ No output generated."
    
        except subprocess.CalledProcessError as e:
            print(f"❌ Subprocess Error:\n{e}")
            print(f"⚠️ stderr Output:\n{e.stderr}")
            return f"❌ Error executing script: {e}"
    
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
            return f"❌ Error executing script: {str(e)}"



# --- 🔹 Main Function to Test the Agent ---
def main():
    agent = gen_ai_script_executer(scripts_path="./scripts")

    # ✅ Test Ansible Execution
    query1 = "get telemetry data of server Win124wrt"
    print("\n🔍 Test Query 1:")
    print(query1)
    print("📢 Result:")
    print(agent.execute_script(query1))

    # # ✅ Test Grafana Execution
    # query2 = "Get data of server name 'grafana-server-05' from Grafana?"
    # print("\n🔍 Test Query 2:")
    # print(query2)
    # print("📢 Result:")
    # print(agent.execute_script(query2))


if __name__ == "__main__":
    main()
