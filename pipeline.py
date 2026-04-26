from agents import research_agent_gemini, reading_agent, search_agent, critic_chain, writer_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}
    
    # Step 1: Search
    print("\n" + "="*40)
    print(" ---------- Step 1: Searching ----------")
    print("="*40)
    
    search = search_agent()
    search_result = search.invoke({
        "messages": [("user", f"Find recent and reliable information about {topic}")]
    })
    
    # create_agent returns the full message list. The AI's final answer is the last one [-1].
    state["search_result"] = search_result["messages"][-1].content
    print("\nSearch results gathered.")

    # Step 2: Reading/Scraping
    print("\n" + "="*40)
    print(" ---------- Step 2: Scraping Top Resources ----------")
    print("="*40)

    reader_agent = reading_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
                      f"Based on the following search results about '{topic}', "
                      f"Pick the most relevant URLs and scrape it for deep content.\n\n"
                      f"Search Results: \n {state['search_result'][:1000]}")]
    })
    
    state['scraped_content'] = reader_result['messages'][-1].content
    print("\n\n ------------------- Scrape content ------------------- \n\n")
    print(state["scraped_content"])

    # Step 3: Writer
    print("\n" + "="*40)
    print(" ---------- Step 3: Writer is drafting the report ----------")
    print("="*40)

    research_combine = (
        f"Search Results\n {state['search_result']} \n\n "
        f"Detailed Scraped content \n {state['scraped_content']}"
    )
    
    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combine
    })

    print("\n ------------ Final Report --------------------\n")
    print(state['report'])

    # Step 4: Critic
    print("\n" + "="*40)
    print(" ---------- Step 4: Critic report ----------")
    print("="*40)

    state['feedback'] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n ----------------------- Critic Feedback -------------------")
    print(state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n\n ------ Enter Research Topic --------: ")
    run_research_pipeline(topic)