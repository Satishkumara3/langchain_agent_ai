import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from research_agent import build_graph
import uuid
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="AI Research Assistant", page_icon="🧬", layout="wide")

# Custom CSS for a premium look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }

    /* Glassmorphism containers */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    .stChatMessage.user {
        background: rgba(56, 189, 248, 0.15);
        border-left: 4px solid #38bdf8;
    }

    .stChatMessage.assistant {
        background: rgba(139, 92, 246, 0.15);
        border-left: 4px solid #8b5cf6;
    }

    /* Gradient Title */
    .title-text {
        font-weight: 600;
        background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Custom Input Box */
    .stChatInputContainer {
        border-radius: 20px !important;
        background-color: rgba(30, 41, 59, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Animation for chat messages */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatMessage {
        animation: fadeIn 0.4s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title-text">🧬 AI Research Assistant</h1>', unsafe_allow_html=True)
st.caption("✨ Intelligent Research powered by LangChain, LangGraph, and Groq")

# Initialize session state for messages and thread_id
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Build the agent graph
@st.cache_resource
def get_agent():
    return build_graph()

agent = get_agent()

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        if msg.content:
            with st.chat_message("assistant"):
                st.markdown(msg.content)

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to session state and display it
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process agent response
    with st.chat_message("assistant"):
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        
        # Display reasoning steps in an expander
        with st.status("🚀 **Analyzing Request...**", expanded=True) as status:
            final_response = ""
            
            # Stream events from the graph
            for event in agent.stream({"messages": st.session_state.messages}, config, stream_mode="values"):
                # Get the latest message
                if "messages" in event:
                    latest_msg = event["messages"][-1]
                    
                    if isinstance(latest_msg, AIMessage):
                        if latest_msg.tool_calls:
                            for tc in latest_msg.tool_calls:
                                st.write(f"🔍 **Executing**: `{tc['name']}`")
                                if tc['name'] == 'tavily_search_results_json':
                                    st.write(f"   *Searching the web for:* {tc['args'].get('query', '')}")
                                elif tc['name'] == 'calculator':
                                    st.write(f"   *Calculating:* {tc['args'].get('expression', '')}")
                        elif latest_msg.content:
                            final_response = latest_msg.content
                    elif isinstance(latest_msg, ToolMessage):
                        st.write(f"✅ **Tool Execution Successful.**")
            
            status.update(label="✨ **Analysis Complete!**", state="complete", expanded=False)
        
        # Display final response
        if final_response:
            st.markdown(final_response)
            st.session_state.messages.append(AIMessage(content=final_response))
        else:
            st.error("Something went wrong. I couldn't generate a response.")

# Sidebar for information
with st.sidebar:
    st.header("About")
    st.write("This Research Assistant uses a multi-step reasoning process to answer complex queries.")
    st.write("### Tools Available:")
    st.write("- **Tavily Search**: Real-time web search")
    st.write("- **Calculator**: High-precision math operations")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
