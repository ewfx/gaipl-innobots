import gradio as gr
from ServiceDesk_LLM import graph_executor  
from gen_ai_script_agent_grafana import gen_ai_script_executer  
from langchain.memory import ConversationBufferMemory
import pandas as pd
import time
import os

#Chatbot with continuous Chat UI.
# Initialize memory for chat history
memory = ConversationBufferMemory()

# Initialize script executor
script_executer = gen_ai_script_executer()

def ask_chatbot(user_query, history):
    """Handles continuous chat, stores & retrieves memory."""
    print("Chatbot query received:", user_query, flush=True)
    
    # Add "AI is typing..." placeholder
    history.append((user_query, "**AI is typing...**"))
    yield "", history  # Update UI with "AI is typing..."

    # Use stored context in the new query
    chat_history = memory.load_memory_variables({})
    
    # Append history to user query for context
    full_query = f"Previous Context:\n{chat_history['history']}\n\nNew Query: {user_query}"
    
    # Simulate AI thinking delay (UX improvement)
    time.sleep(0.05)

    # Invoke LangGraph with context
    response = graph_executor.invoke({"query": full_query})
    chatbot_response = response["Final_Response"]
    
    # Save current query-response pair to memory
    memory.save_context({"query": user_query}, {"response": chatbot_response})
    
    print("Chatbot response:", chatbot_response, flush=True)
    
    # Replace "AI is typing..." with actual response
    history[-1] = (user_query, chatbot_response)
    
    yield "", history  # Update chat with actual response

def run_script(user_query):
    """Executes a script based on user input."""
    print("Script query received:", user_query, flush=True)
    
    result = script_executer.execute_script(user_query)
    
    print("Script execution result:", result, flush=True)
    return result

def clear_chat():
    """Clears chat history."""
    memory.clear()  # Clears stored memory
    return []

# 🚀 Define Gradio UI with Enter key submission, typing indicator & clear chat button
with gr.Blocks() as demo:
    gr.Markdown("## GenAI-Powered Integrated Platform Environment")
    
    with gr.Tabs():
        # Chat Bot Tab
        with gr.TabItem("SmartOps ChatBot"):
            gr.Markdown("### SmartOps AI – Ready to Assist!")
            
            chatbot_ui = gr.Chatbot(label="Chat History")  # Continuous chat interface
            user_input = gr.Textbox(label="Type your message...", placeholder="E.g., How many Windows servers are active?", show_label=False)
            clear_button = gr.Button("Clear Chat")

            # Enter Key or Submit Button inside Textbox
            user_input.submit(fn=ask_chatbot, inputs=[user_input, chatbot_ui], outputs=[user_input, chatbot_ui])

            # Clear Chat Button
            clear_button.click(fn=clear_chat, inputs=[], outputs=[chatbot_ui])

        # Script Execution Tab
        with gr.TabItem("Agentic Innobot"):
            gr.Markdown("### AI-Powered Action Hub")
            
            script_input = gr.Textbox(label="Agentic Query", placeholder='E.g., Please get data of XYZ server from Grafana?', show_label=False)
            script_output = gr.Textbox(label="Agentic Hub Response", interactive=False)
            
            # Enter Key Submission for Script Execution
            script_input.submit(fn=run_script, inputs=script_input, outputs=script_output)

# 🚀 Launch the Gradio App
if __name__ == "__main__":
    print("Launching Gradio App...")
    demo.launch()