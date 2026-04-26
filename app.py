import streamlit as st
from agents import search_agent, reading_agent, writer_chain, critic_chain

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(page_title="Auto-Researcher Pro", page_icon="🧠", layout="wide")

# Inject some custom CSS to make things look a bit more polished
st.markdown("""
    <style>
    .main-header {text-align: center; font-family: 'Helvetica Neue', sans-serif; color: #1E88E5;}
    .sub-header {text-align: center; color: #616161; margin-bottom: 30px;}
    .stButton>button {background-color: #1E88E5; color: white; border-radius: 8px; font-weight: bold;}
    .stButton>button:hover {background-color: #1565C0; color: white;}
    </style>
""", unsafe_allow_html=True)

# --- 2. Sidebar: How it Works (Architecture Explanation) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103284.png", width=100) # Placeholder AI icon
    st.title("⚙️ Under the Hood")
    st.write("This app uses a **Multi-Agent Pipeline** to autonomously research and write about any topic.")
    
    st.divider()
    st.subheader("🤖 The Agents")
    
    st.markdown("""
    **1. Search Agent (Llama 3.1 8B)**
    * **Role:** The Scout.
    * **Action:** Uses the *Tavily API* to scour the web for the most recent and relevant sources.
    
    **2. Reading Agent (Mistral Small)**
    * **Role:** The Scholar.
    * **Action:** Visits the URLs found by the Search Agent and scrapes the raw HTML, filtering out junk to extract deep context.
    
    **3. Writer Agent (Gemini 2.5 Flash)**
    * **Role:** The Author.
    * **Action:** Synthesizes the raw data and search snippets into a highly structured, professional report.
    
    **4. Critic Agent (Gemini 2.5 Flash)**
    * **Role:** The Editor.
    * **Action:** Reviews the final report, scores it out of 10, and highlights strengths and areas for improvement.
    """)
    st.divider()
    st.caption("Built with LangChain, Streamlit, Groq, Mistral, and Google Gemini.")

# --- 3. Main UI Header ---
st.markdown("<h1 class='main-header'>🧠 Auto-Researcher Pro</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-header'>Deploy an autonomous AI team to research any topic in seconds.</h4>", unsafe_allow_html=True)

# --- 4. Centered Search Interface ---
# Using columns to center the input box makes it look much more modern
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    topic = st.text_input("What would you like to research?", placeholder="e.g., The future of AI in Medical Imaging 2026")
    run_button = st.button("🚀 Launch Research Agents", use_container_width=True)

st.divider()

# --- 5. Execution Pipeline ---
if run_button:
    if not topic.strip():
        st.toast("⚠️ Please enter a topic first!", icon="🚨")
    else:
        state = {}
        
        # Live Status Updater
        with st.status("Initializing AI Agents... Standby.", expanded=True) as status:
            
            # Step 1: Searching
            st.write("🔍 **Agent 1 (Search):** Querying Tavily for top sources...")
            search = search_agent()
            search_result = search.invoke({
                "messages": [("user", f"Find recent and reliable information about {topic}")]
            })
            state["search_result"] = search_result["messages"][-1].content
            
            # Step 2: Scraping
            st.write("📖 **Agent 2 (Reading):** Extracting deep context from URLs...")
            reader_agent = reading_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                              f"Based on the following search results about '{topic}', "
                              f"Pick the most relevant URLs and scrape it for deep content.\n\n"
                              f"Search Results: \n {state['search_result'][:1000]}")]
            })
            state['scraped_content'] = reader_result['messages'][-1].content
            
            # Step 3: Writing
            st.write("✍️ **Agent 3 (Writer):** Synthesizing data into a report...")
            research_combine = (
                f"Search Results\n {state['search_result']} \n\n "
                f"Detailed Scraped content \n {state['scraped_content']}"
            )
            state['report'] = writer_chain.invoke({
                "topic": topic,
                "research": research_combine
            })
            
            # Step 4: Critiquing
            st.write("⚖️ **Agent 4 (Critic):** Evaluating report quality...")
            state['feedback'] = critic_chain.invoke({
                "report": state['report']
            })
            
            status.update(label="✅ Research Complete!", state="complete", expanded=False)

        # --- 6. Beautiful Results Display (Tabs) ---
        # Tabs keep the UI from getting too long and messy
        st.success("Pipeline executed successfully. View your results below.")
        
        tab_report, tab_critic, tab_raw = st.tabs(["📄 Final Report", "🧐 Critic's Review", "📊 Raw Data Flow"])
        
        with tab_report:
            st.markdown(state['report'])
            
        with tab_critic:
            st.info("The Critic Agent evaluates the report based on structure, accuracy, and clarity.")
            st.markdown(state['feedback'])
            
        with tab_raw:
            st.markdown("### 1. What the Search Agent Found")
            st.text(state["search_result"])
            st.divider()
            st.markdown("### 2. What the Reading Agent Scraped")
            st.text(state["scraped_content"])