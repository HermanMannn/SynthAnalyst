import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM


load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("Error: GEMINI_API_KEY not found. Please check your .env file.")

# 2. Initialize the Gemini LLM (using gemini-2.5-flash for speed and cost-efficiency)
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
)


market_researcher = Agent(
    role="Senior Market Researcher",
    goal="Gather the latest news and sentiment on NASDAQ futures and Bitcoin.",
    backstory="You are a veteran financial researcher with a knack for spotting early market trends.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

financial_analyst = Agent(
    role="Chief Financial Analyst",
    goal="Analyze market data and write a concise market brief.",
    backstory="You distill complex financial data into clear, actionable insights for investors.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

research_task = Task(
    description="Search for the latest breaking news regarding NASDAQ futures and Bitcoin. Summarize the top 3 headlines and general market sentiment.",
    expected_output="A bulleted summary of top headlines and overall market sentiment.",
    agent=market_researcher
)

analysis_task = Task(
    description="Using the research provided, write a short, 2-paragraph market brief explaining the potential impacts on the tech sector and the crypto market.",
    expected_output="A 2-paragraph market brief with insights on tech and crypto.",
    agent=financial_analyst
)


market_crew = Crew(
    agents=[market_researcher, financial_analyst],
    tasks=[research_task, analysis_task],
    process=Process.sequential
)

if __name__ == "__main__":
    print("🚀 Starting the CrewAI Workflow...")
    result = market_crew.kickoff()
    
    print("\n" + "="*40)
    print("📈 FINAL ANALYSIS BRIEF:")
    print("="*40 + "\n")
    print(result)