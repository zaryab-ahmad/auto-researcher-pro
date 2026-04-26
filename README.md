# 🧠 Auto-Researcher Pro: Multi-Agent AI Research System

Auto-Researcher Pro is an autonomous, multi-agent AI system designed to streamline the research process. Built with **LangChain** and **Streamlit**, it deploys specialized AI agents to search the web, read deep content, write structured reports, and critique the final output.

## 🚀 Features

* **Multi-Agent Architecture**: Divides the research workload across specialized LLMs for optimal speed and reasoning.
* **Autonomous Web Searching**: Uses the Tavily API to find the most relevant, up-to-date sources.
* **Deep Web Scraping**: Automatically extracts and cleans text from target URLs, filtering out HTML noise.
* **Intelligent Synthesis**: Compiles raw data into a professional, well-structured insight report.
* **Self-Critique Mechanism**: An independent critic agent reviews the final report and provides actionable feedback.
* **Beautiful UI**: A modern, responsive Streamlit web interface with interactive tabs and live progress tracking.

## 🛠️ Tech Stack

* **Frameworks:** LangChain, Streamlit
* **Models:**
  * **Search Agent:** Llama-3.1-8b-instant (via Groq)
  * **Reading Agent:** Mistral-small-latest (via Mistral AI)
  * **Writer & Critic Agents:** Gemini-2.5-flash (via Google Gemini)
* **Tools:** Tavily Search API, BeautifulSoup (Web Scraping)

## 📦 Installation & Setup

## **1. Clone the repository**
```bash
git clone [https://github.com/yourusername/auto-researcher-pro.git](https://github.com/yourusername/auto-researcher-pro.git)
cd auto-researcher-pro
```
## **2. Create and activate a virtual environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```
## **3. Install dependencies**
```bash
pip install -r requirements.txt
```
## **4. Set up Environment Variables**
Create a .env file in the root directory and add your API keys:
```bash
GROQ_API_KEY=your_groq_api_key
MISTRAL_API_KEY=your_mistral_api_key
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```
## 💻 Usage
To launch the Streamlit web application, run the following command in your terminal:<br>
`streamlit run app.py`

This will automatically open the web interface in your default browser. Enter any topic into the search bar, and watch the agents work together to build your research report!

## 📂 Project Structure
- app.py: The Streamlit frontend and UI configuration.

- agents.py: Contains the logic for the LangChain agents and prompt templates.

- create_tools.py: Defines the web_search and web_scrape tools used by the agents.

- requirements.txt: Python package dependencies.

## 📝 License
This project is licensed under the MIT License.