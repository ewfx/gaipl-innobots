## Prompts for each Agents

# 1.	Device Search Agent UI Prompt

Search for network devices by any attribute:

- Device ID (e.g., "R001", "S001A", "FW001")
- Device type (e.g., "router", "switch", "firewall")
- Location (e.g., "NYC", "SFO", "Data Center")
- Status (e.g., "active", "warning", "inactive")
- Importance (e.g., "critical", "high", "medium")

Prompt : You can combine attributes (e.g., "critical routers in NYC") or search for specific devices (e.g., "Find router R001").

Expected Result: The system will identify matching devices and show their relationships to other devices in the network.

# 2.	Troubleshooting Agent UI Prompt

Describe the network issue you're experiencing:
- Provide specific error messages or symptoms
- Mention affected devices if known
- Include when the problem started
- Note any recent changes that might be related

Prompt: "Users can't access the customer portal since 9am. Error logs show connection timeouts to the application server. No recent changes were made to the network."
Expected Result:The system will analyze the issue and suggest troubleshooting steps

# 3.	Knowledge Base Agent UI Prompt

Search the network knowledge base:
- Ask about protocols (e.g., "How does BGP route selection work?")
- Request best practices (e.g., "Firewall configuration guidelines")
- Query about specific technologies (e.g., "QoS implementation options")
- Seek procedural information (e.g., "Steps to implement HSRP")

(Optionally)select a document type to focus your search on specific resources (manuals, guides, references, etc.).

Expected Result: The system will provide relevant information with citations from trusted sources.

# 4.	Observability Agent UI Prompt

Select network components and metrics to analyze:
- CI Types: Choose device categories to monitor (routers, switches, firewalls)
- Metrics: Select performance indicators (CPU, memory, latency, errors)
- Time Range: Specify the period for analysis (last hour to last week)

Prompt:: Analyze CPU and memory utilization on all routers over the last 24 hours.

Expected Result:The system will assess the metrics against baselines and identify any concerning patterns.

# 5.	Incident Resolution Agent UI Prompt

Provide incident details for analysis:
- Incident ID: A unique identifier for tracking
- Title: Brief description of the issue
- Description: Detailed explanation of what happened
- Status: Current state (open, in progress, resolved)
- Priority: Impact level (critical, high, medium, low)
- Affected CIs: Devices or services impacted (comma-separated)

Expected Result: The system will generate an incident report with root cause analysis and recommended actions.
