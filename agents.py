import os
from dotenv import load_dotenv

# LangChain Core Imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# The new LangChain v1.0 standard import
from langchain.agents import create_agent

# Model Providers
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Custom Tools
from create_tools import web_search, web_scrape

load_dotenv()

# --- Model Setup ---
research_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
reading_llm = ChatMistralAI(model="mistral-small-latest", temperature=0.2)
gemini_call = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# --- Agent Functions ---
# Notice we use 'model=' instead of 'llm=' in the new create_agent
def search_agent():
    return create_agent(
        model=research_llm, 
        tools=[web_search],
        system_prompt="You are an expert researcher. Use tools to find information."
    )

def reading_agent():
    return create_agent(
        model=reading_llm, 
        tools=[web_scrape],
        system_prompt="You are an expert reader. Scrape URLs and extract important details."
    )

def research_agent_gemini():
    return create_agent(
        model=gemini_call, 
        tools=[web_scrape, web_search],
        system_prompt="You are an expert research assistant."
    )

# --- Writer Chain ---
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear and structured insight reports."),
    ("human", """Write a detailed research report on the topic below.
    Topic: {topic}
    Research Gathered: {research}

    Structure report as:
    - Introduction
    - Key findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs)
    """)
])

writer_chain = writer_prompt | gemini_call | StrOutputParser()

# --- Critic Chain ---
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic."),
    ("human", "Review this report critically:\n\n{report}")
])

critic_chain = critic_prompt | gemini_call | StrOutputParser()