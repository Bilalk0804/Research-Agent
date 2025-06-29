import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from pydantic import BaseModel
from tools import search_tool, wiki_tool, save_tool
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .research-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .source-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .tool-badge {
        background: #17a2b8;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'research_results' not in st.session_state:
    st.session_state.research_results = []

# Pydantic model for structured output
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize the model and tools
@st.cache_resource
def initialize_model():
    """Initialize the LLM model and tools (cached to avoid reloading)"""
    try:
        llm = init_chat_model(
            "mistralai/mixtral-8x7b-instruct-v0.1", 
            model_provider="Nvidia", 
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        
        parser = PydanticOutputParser(pydantic_object=ResearchResponse)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert research assistant powered by AI. Your job is to gather concise, high-quality insights on a given topic using custom tools (e.g., search, Wikipedia, academic databases). For each topic, follow this structure:

            1. Provide a **concise summary** (150–300 words) explaining the topic clearly.
            2. List **credible sources** used, with links if available.
            3. Mention the **tools or methods** you used to find the information (e.g., Wikipedia wrapper, Google Search tool, academic search).
            4. Present all content in the following format (no extra commentary):
            5. Make use of the tools provided to you, such as search and Wikipedia, to gather information.
            {format_instructions}

            Avoid vague responses. If you cannot find information, state clearly which part failed and suggest next steps for research.
            """),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}")
        ]).partial(format_instructions=parser.get_format_instructions())
        
        tools = [search_tool, wiki_tool, save_tool]
        agent = create_tool_calling_agent(
            llm=llm,
            prompt=prompt,
            tools=tools
        )
        
        return llm, agent, tools, parser
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return None, None, None, None

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 AI Research Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Mixtral-8x7B and LangChain</p>', unsafe_allow_html=True)
    
    # Initialize model and tools once
    llm, agent, tools, parser = initialize_model()
    
    # Check if initialization was successful
    if llm is None or agent is None or tools is None or parser is None:
        st.error("❌ Failed to initialize the model. Please check your API key and try again.")
        st.stop()
    
    # Type assertions to help linter
    assert llm is not None
    assert agent is not None  
    assert tools is not None
    assert parser is not None
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model status
        st.subheader("Model Status")
        st.success("✅ Model loaded successfully")
        
        # Tools info
        st.subheader("🛠️ Available Tools")
        tool_names = [tool.name for tool in tools]
        for tool_name in tool_names:
            st.write(f"• {tool_name}")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.session_state.research_results = []
            st.rerun()
        
        # Export results
        if st.session_state.research_results:
            st.subheader("📊 Export")
            if st.button("💾 Export Results"):
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "research_results": st.session_state.research_results
                }
                st.download_button(
                    label="📥 Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"research_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Research Query")
        
        # Query input
        query = st.text_area(
            "Enter your research topic or question:",
            placeholder="e.g., What are the latest developments in quantum computing?",
            height=100
        )
        
        # Research button
        if st.button("🔍 Start Research", type="primary"):
            if query.strip():
                with st.spinner("🔬 Researching your topic..."):
                    try:
                        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
                        raw_response = agent_executor.invoke({"query": query})
                        
                        # Parse the structured response
                        structured_response = parser.parse(raw_response['output'])
                        
                        # Store in session state
                        st.session_state.research_results.append({
                            "query": query,
                            "response": structured_response.dict(),
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        st.success("✅ Research completed!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during research: {str(e)}")
            else:
                st.warning("⚠️ Please enter a research query.")
    
    with col2:
        st.subheader("📈 Quick Stats")
        if st.session_state.research_results:
            st.metric("Total Queries", len(st.session_state.research_results))
            st.metric("Last Research", "Today" if st.session_state.research_results else "Never")
        else:
            st.info("No research completed yet.")
    
    # Display research results
    if st.session_state.research_results:
        st.subheader("📋 Research Results")
        
        for i, result in enumerate(reversed(st.session_state.research_results)):
            with st.expander(f"🔍 {result['query']} - {datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M')}", expanded=True):
                response = result['response']
                
                # Research card
                st.markdown(f"""
                <div class="research-card">
                    <h3>📝 Summary</h3>
                    <p>{response['summary']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Sources
                if response['sources']:
                    st.subheader("📚 Sources")
                    for source in response['sources']:
                        st.markdown(f"""
                        <div class="source-card">
                            {source}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tools used
                if response['tools_used']:
                    st.subheader("🛠️ Tools Used")
                    for tool in response['tools_used']:
                        st.markdown(f'<span class="tool-badge">{tool}</span>', unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"💾 Save to File", key=f"save_{i}"):
                        try:
                            # Import the save function directly from tools
                            from tools import save_to_txt
                            save_to_txt(json.dumps(response, indent=2), f"research_{i+1}.txt")
                            st.success("Saved to file!")
                        except Exception as e:
                            st.error(f"Error saving: {e}")
                
                with col2:
                    if st.button(f"📋 Copy Summary", key=f"copy_{i}"):
                        st.write("Summary copied to clipboard!")
                        st.code(response['summary'])
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                        st.session_state.research_results.pop(-(i+1))
                        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>🔍 AI Research Assistant | Powered by Mixtral-8x7B & LangChain</p>
            <p>Built with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 