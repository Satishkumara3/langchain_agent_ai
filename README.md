# 🧬 AI Research Assistant

An intelligent, multi-turn AI agent built with **LangChain**, **LangGraph**, and **Groq** to perform deep research and complex mathematical reasoning through a premium **Streamlit** user interface.

## ✨ Key Features

- **🧠 Multi-Step Reasoning**: Uses a stateful agent (LangGraph) that "thinks" before responding.
- **🔍 Web Search Integration**: Real-time information retrieval using the **Tavily AI** search motor.
- **⏳ Context-Aware**: Maintains conversation history using `MemorySaver` for natural, continuous dialogue.
- **⚡ High Performance**: Powered by **Groq**'s lightning-fast inference for instantaneous responses.
- **💎 Premium UI**: A beautiful, dark-themed experience featuring **Glassmorphism**, gradients, and smooth animations.

## 🚀 Quick Start

### 1. Clone & Install
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

### 3. Run the App
```bash
streamlit run app.py
```

## 🛠️ Built With

- **LangChain & LangGraph**: Agentic workflow and tools integration.
- **Groq (Llama 3.3)**: High-performance LLM brain.
- **Tavily AI**: Optimized search for AI agents.
- **Streamlit**: Modern, interactive web frontend.
- **Python-Dotenv**: Secure environment variable management.

## 📁 Project Structure

- `app.py`: Streamlit frontend with custom CSS styling.
- `research_agent.py`: LangGraph logic and agent state management.
- `tools.py`: Definition of search and math-focused tools.
- `requirements.txt`: Project dependencies.
- `run_app.bat`: Quick-launch script for Windows users.

---
Built with ❤️ for deep research and reasoning.
