# 🚀 Project Name
Integrated Platform Enviornment - Gen AI for Platform Support by Team Innobots

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Develop a Gen-Al enabled Integrated Platform Environment (IPE) that provides an integrated console to our platform support teams providing them following capabilities

- Provide agentic capabilities for incident resolution
- Al chatbot to contextually chat with a GPT backend on the incident/issue that they are resolving at the moment
- Contextual recommendations with telemetry, related incidents
- Ability to leverage enterprise information for troubleshooting
- Context based data extraction: Extract fields like connectivity information, upstream and downstream dependency based on simple query for the Cl in question

## 🎥 Demo
Location - Artifacts/demo/app1
- 🔹 Agentic Innobot
- 🔹 SmartOps ChatBot

Location - Artifacts/demo/app2
- 🔹 Starting the Gradio UI App
- 🔹 Agent-Device Search
- 🔹 Agent - Troubleshooting
- 🔹 Agent - Observability
- 🔹 Agent - Knowledge Base
- 🔹 Agent - Incident Response

## 💡 Inspiration
Currently Technology organization has a large platform support system operations organization that provides application and infrastructure support across L1/L2/L3 levels for our application and infrastructure platforms. Platform support requires troubleshooting, accessing variety of KB (Knowledge base) articles, running ansible automation scripts, reviewing telemetry / observability metrics as well as leveraging foundational information about the Cis (Configuration items) including their relationships, dependencies, health etc. etc. All these tools and products require frequent context switching, cause significant time/effort overhead in accessing different tools, portals to provide the required platform support for the technology environment.

So this chatbot having agentic workflows provides an integrated console to our platform support teams providing them the Single Frame of View and Data Information from across the tools which are used by the Operations team.

## ⚙️ What It Does
We have tried to implment two flows: Chat Flow (For User Interactions) and Multi-Agent Flow (Trigger)
# Chat Flow - /artifacts/arch/Flows/UserFlow.png
- AI chatbot to contextually chat with a GPT backend on the Context based data extraction of the CI Items - Like Location, Environment, Support Groups and CI related information required by the Operations Engineers.
- Provide agentic capabilities for monitoring of those CI Items and viewing the Time-Series Data of the CI Item (MCP implmenation with Grafana\Prometheus)
- Context based data extraction where it can provide upstream and downstream dependency based on simple query for the CI in question.

# Trigger Based Autonomous Flow - /artifacts/arch/Flows/TriggerBasedAutonomousFlow.png
- Ability to leverage enterprise information for troubleshooting, where it can integrate with data source using MCP (Model context protocol) to take action which can be either: Invasive (Which changes something on the CI Item) and Non-Invasive (Information Gathering on the CI Item). 
- Invasive actions will further require Approvals - Man in the loop
- Non-Invasive will only be used for information gathering and does not require approval - Man outside of the loop
- Multi-Agents will work in tandem where a second agent can just monitor the status what the first agent is doing and third agent can run the live probe to validate the CI status.

## 🛠️ How We Built It - /artifacts/arch/Architecture-Design.pdf

🔹 Gradio UI: UI is developed using Gradio for interation with Data through MCP -> LLM ->RAG/LangGraph
- Device Search
- Troubleshooting
- Observability
- Knowledge Base
- Incident Response

🔹 MCP Framework:
- Agent Registry: Routes query to Agents
- Agent Context: Maintains shared content,Remembers entities
- Specialized Agents:Device search Agent, TS Agent... 
- Knowledge Integration: Cross-Agent knowledge,context enrichment,Query enhancement

🔹 LLM Layer:
- Model : TinyLlama
- Optimized Prompting

🔹 LangGraph Layer: LangGraph Enabled Device Search provide
- Structured Workflow Management - Edge/Node definition
- Query Parsing - Device Search - Topology Analysis for device relationships -Result Formatting

🔹 RAG Layer: Specialized Agents Accomplish Tasks based on their domain expertise/definition
- Vector Stores: Troubleshooting, Device Search,KB, Cross-search store
- Document Processing: Text chunking,Embedding,Section mapping,Formatting
- Knowledge Base: KB Articles

## 🚧 Challenges We Faced
- Using the TinyLlama required GPU for the LLM to train. On CPU, it is slow.
- MCP Implementations require connections for Enterprise API
- Chroma DB hosting requires specific hardware for scability. For demo, it is a single-point of failure.
- RAG implementation requires Enterprise Data inventory which could have helped with upstream and downstream correlations.
- Dataset was not available for the training. We created sample dataset for the training but it does not cover all the possibile combinations of relationships.

## 🏃 How to Run - /artifacts/arch/Demo-Flows-Innobots.docx
1. Clone the repository  
   ```
   git clone https://github.com/ewfx/gaipl-innobots.git
   ```
2. Install dependencies  
   ```
   pip install -r requirements.txt
   ```
3. Run the project : One app only
   ```
   App1: python .\code\src\app1\Gradio_GenAI_Agent.py
   App1(Unix): python /code/src/app1/Gradio_GenAI_Agent.py
   App2: python .\code\src\update_gradio_app.py
   App2(Unix): python /code/src/update_gradio_app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: Python - Gradio
- 🔹 Backend: Python
- 🔹 Database: ChromaDB
- 🔹 LLM: TinyLlama/TinyLlama-1.1B-Chat-v1.0 (LLM)
- 🔹 Embeddings Used: sentence-transformers/all-MiniLM-L6-v2
- 🔹 Hardware Used : For best results, Use GPU for execution of the code and UI

## 👥 Team
- **Keshri Anand**
- **Vani Padmanabha**
- **Abhishek Malviya**
- **Sureshkumar Gangeswaran**
- **Jatin Aggarwal**