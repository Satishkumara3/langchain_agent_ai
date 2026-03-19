import os
from typing import Annotated, List, Union, TypedDict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from tools import get_tools

load_dotenv()

# Define the state for the graph
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]

# Define the nodes
def call_model(state: AgentState):
    messages = state['messages']
    
    # System prompt to guide the agent
    system_msg = {
        "role": "system",
        "content": "You are a helpful AI Research Assistant. You can use the search tool to find information online and the calculator tool for math. Always provide clear, concise, and accurate answers. Be transparent about your sources when using the search tool."
    }
    
    # Prepend system message if it's the start of a conversation
    if len(messages) == 1:
        messages = [system_msg] + messages
    
    # Initialize implementation of ChatGroq
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile", # High performance free model
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def build_graph():
    # Initialize tools and ToolNode
    tools = get_tools()
    tool_node = ToolNode(tools)
    
    # Define the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    def should_continue(state: AgentState):
        messages = state['messages']
        last_message = messages[-1]
        
        # If the LLM makes a tool call, then we continue to the tools node
        if last_message.tool_calls:
            return "tools"
        # Otherwise, we stop (reply to the user)
        return END

    workflow.add_conditional_edges(
        "agent",
        should_continue,
    )
    
    # Add normal edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Initialize memory to persist state between graph runs
    checkpointer = MemorySaver()
    
    # Finally, compile the graph
    return workflow.compile(checkpointer=checkpointer)

# Example usage
if __name__ == "__main__":
    app = build_graph()
    config = {"thread_id": "1"}
    
    input_message = HumanMessage(content="What is the current stock price of Nvidia and what is its square root?")
    
    for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
        for value in event.values():
            print(value[-1].content if hasattr(value[-1], 'content') else value[-1])
