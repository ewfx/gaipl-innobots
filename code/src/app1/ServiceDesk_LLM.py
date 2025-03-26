import os
import openai
import pandas as pd
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langgraph.graph import StateGraph, END
import json
import logging
from typing import TypedDict, List
from langchain.schema import Document
import openai
import pandas as pd


api_key = ""

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize OpenAI Models
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=api_key)

#With Langchain and Langgraph

import os
import json
import logging
import pandas as pd
from typing import TypedDict, List

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

import langgraph
from langgraph.graph import StateGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI Models
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=api_key)

# Data sources
DATA_SOURCES = {
    "Change_Requests": "Change_Request.xlsx",
    "CI_Data": "CI_Data.xlsx",
    "Knowledge_Base": "Knowledge_Base.xlsx",
    "Database_Data": "Database_Data.xlsx",
    "Incidents": "Incidents_Data.xlsx",
    "Network_Devices": "Network_Devices.xlsx"
}


class OpenAI_RAG:
    """Handles RAG-based retrieval for each data source."""

    def __init__(self, docs_path: str, persist_directory: str):
        self.docs_path = docs_path
        self.persist_directory = persist_directory
        self.vector_stores = {}

    def _load_documents(self, file_path, source):
        """Load and chunk Excel data into documents."""
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            row_text = " | ".join(f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col]))
            if row_text.strip():
                docs = text_splitter.split_text(row_text)
                documents.extend([Document(page_content=doc, metadata={"source": source}) for doc in docs])

        return documents

    def _create_vector_store(self, source_name, file_path):
        """Create vector store for a data source."""
        logger.info(f"Processing data for: {source_name}")
        docs = self._load_documents(file_path, source_name)

        self.vector_stores[source_name] = Chroma.from_documents(
            documents=docs,
            embedding=embedding_model,
            persist_directory=os.path.join(self.persist_directory, source_name)
        )
        self.vector_stores[source_name].persist()
        logger.info(f"Vector store created for {source_name}")

    def setup_rag(self):
        """Initialize vector stores for all sources."""
        for source, filename in DATA_SOURCES.items():
            file_path = os.path.join(self.docs_path, filename)
            if not os.path.exists(file_path):
                logger.warning(f"{filename} not found. Skipping...")
                continue

            vector_store_path = os.path.join(self.persist_directory, source)
            if not os.path.exists(vector_store_path) or not os.listdir(vector_store_path):
                self._create_vector_store(source, file_path)
            else:
                self.vector_stores[source] = Chroma(
                    persist_directory=vector_store_path,
                    embedding_function=embedding_model
                )

    def retrieve_relevant_docs(self, query: str, source: str, k: int = 50):
        """Retrieve relevant documents from a specific source."""
        if source not in self.vector_stores:
            return []
        
        return self.vector_stores[source].similarity_search(query, k=k)


# Initialize RAG system
docs_path = "./documents"
persist_directory = "./chroma_db"
rag_system = OpenAI_RAG(docs_path, persist_directory)
rag_system.setup_rag()

import json
import logging
from typing import List

class ServiceDesk_LLM:
    """LangGraph-based orchestration for querying multiple sources with Model Context Processing (MCP)."""

    def __init__(self, rag_system, memory_limit=5):
        """
        Initializes the ServiceDesk LLM with MCP and memory constraints.

        Args:
            rag_system: Instance of OpenAI_RAG for document retrieval.
            memory_limit: Number of queries to retain before context expires.
        """
        self.rag_system = rag_system
        self.memory_limit = memory_limit

        # MCP: Context Memory for each data category
        self.context_memory = {
            "CI": [],
            "Change": [],
            "Network": [],
            "DB": [],
            "Incidents": []
        }

        # Memory counter to track expiration
        self.memory_counter = {
            "CI": 0,
            "Change": 0,
            "Network": 0,
            "DB": 0,
            "Incidents": 0
        }

    def _retrieve_with_memory(self, query, source, category):
        """Retrieves data from memory if available; otherwise, queries ChromaDB."""
        
        # Step 1: Check if the memory exists
        if self.context_memory[category]:
            logging.info(f"📌 Using MCP Context Memory for {category}")
            return self.context_memory[category]

        # Step 2: Query ChromaDB if memory is empty
        results = self.rag_system.retrieve_relevant_docs(query, source)

        # Step 3: Store results in MCP memory (limit to avoid memory overflow)
        if results:
            self.context_memory[category].extend(results)
            self.memory_counter[category] += 1  # Increase counter

            # Step 4: Expire memory if limit is reached
            if self.memory_counter[category] >= self.memory_limit:
                logging.info(f"🧹 Expiring memory for {category} after {self.memory_limit} queries")
                self.context_memory[category] = []  # Reset memory
                self.memory_counter[category] = 0  # Reset counter

        return results

    def retrieve_from_ci(self, state):
        """Retrieve CI data with MCP context memory."""
        return {"CI_Results": self._retrieve_with_memory(state["query"], "CI_Data", "CI")}

    def retrieve_from_change(self, state):
        """Retrieve Change Request data with MCP context memory."""
        return {"Change_Results": self._retrieve_with_memory(state["query"], "Change_Requests", "Change")}

    def retrieve_from_network(self, state):
        """Retrieve Network data with MCP context memory."""
        return {"Network_Results": self._retrieve_with_memory(state["query"], "Network_Devices", "Network")}

    def retrieve_from_db(self, state):
        """Retrieve Database data with MCP context memory."""
        return {"DB_Results": self._retrieve_with_memory(state["query"], "Database_Data", "DB")}

    def retrieve_from_incidents(self, state):
        """Retrieve Incident data with MCP context memory."""
        return {"Incident_Results": self._retrieve_with_memory(state["query"], "Incidents", "Incidents")}

    def format_response(self, state):
        """Format response with full context memory for better readability."""
        
        def extract_text(docs):
            """Extracts clean text from Document objects."""
            return [doc.page_content for doc in docs] if docs else []

        # Structure response with retained memory context
        results = {
            "CI Data": extract_text(self.context_memory["CI"]),
            "Change Requests": extract_text(self.context_memory["Change"]),
            "Network Data": extract_text(self.context_memory["Network"]),
            "Database Info": extract_text(self.context_memory["DB"]),
            "Incident Reports": extract_text(self.context_memory["Incidents"]),
        }

        # Convert structured data to JSON
        formatted_results = json.dumps(results, indent=2)

        # Pass formatted response to LLM for final answer generation
        final_prompt = f"Context:\n{formatted_results}\n\nUser Query: {state['query']}\n\nAnswer:"
        response = llm.predict(final_prompt)

        return {"Final_Response": response}
        

# Define the state schema for LangGraph
class ServiceDeskState(TypedDict):
    query: str
    CI_Results: List[str]
    Change_Results: List[str]
    Network_Results: List[str]
    DB_Results: List[str]
    Incident_Results: List[str]
    Final_Response: str


# Initialize LangGraph workflow
workflow = StateGraph(state_schema=ServiceDeskState)
service_desk_llm = ServiceDesk_LLM(rag_system)

# Define the START node
workflow.add_node("START", lambda state: {"query": state["query"]})

# Add search nodes
workflow.add_node("CI_Search", service_desk_llm.retrieve_from_ci)
workflow.add_node("Change_Search", service_desk_llm.retrieve_from_change)
workflow.add_node("Network_Search", service_desk_llm.retrieve_from_network)
workflow.add_node("DB_Search", service_desk_llm.retrieve_from_db)
workflow.add_node("Incident_Search", service_desk_llm.retrieve_from_incidents)
workflow.add_node("Format_Response", service_desk_llm.format_response)

# Define edges: START ➝ Search Nodes
workflow.add_edge("START", "CI_Search")
workflow.add_edge("START", "Change_Search")
workflow.add_edge("START", "Network_Search")
workflow.add_edge("START", "DB_Search")
workflow.add_edge("START", "Incident_Search")

# Search Nodes ➝ Format Response
workflow.add_edge("CI_Search", "Format_Response")
workflow.add_edge("Change_Search", "Format_Response")
workflow.add_edge("Network_Search", "Format_Response")
workflow.add_edge("DB_Search", "Format_Response")
workflow.add_edge("Incident_Search", "Format_Response")

# Define the workflow entry point
workflow.set_entry_point("START")

# Compile LangGraph workflow
graph_executor = workflow.compile()


# # 🔹 MAIN FUNCTION: Run a test query
# def main():
#     query = "How many total Windows servers are there?"
#     response = graph_executor.invoke({"query": query})
#     print("\n=== Generated Response ===")
#     print(response["Final_Response"])

def main():
    # First query (adds data to context)
    query1 = "What is Device ID of Device Name RLSTP01R08?"
    response1 = graph_executor.invoke({"query": query1})
    print("\n=== First Query Response ===")
    print(response1["Final_Response"])

    # Second query (uses stored context)
    query2 = "What is location of Device Name RLSTP01R08?"
    response2 = graph_executor.invoke({"query": query2})
    print("\n=== Follow-up Query Response ===")
    print(response2["Final_Response"])

    query3 = "What is Device ID of Device Name RLSTP01R08?"
    response3 = graph_executor.invoke({"query": query3})
    print("\n=== Follow-up Query Response ===")
    print(response3["Final_Response"])

if __name__ == "__main__":
    main()