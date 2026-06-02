import os
import urllib.request
import json
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from langchain_community.document_loaders import WebBaseLoader

# Load environment variables
load_dotenv()

app = FastAPI(title="SynthAnalyst Intelligence Engine")

# Initialize Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.3,
    api_key=os.environ.get("GEMINI_API_KEY")
)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = "C0B8J04S49E"  # your all-testapi channel


class AnalysisRequest(BaseModel):
    competitor_url: str
    target_role: str = "Sales Representative"


def scrape_competitor_site(url: str) -> str:
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        if not docs:
            return "Failed to scrape website: No content found."
        return docs[0].page_content[:2000]
    except Exception as e:
        return f"Failed to scrape website: {str(e)}"


def post_to_slack(message: str):
    payload = json.dumps({
        "channel": SLACK_CHANNEL_ID,
        "text": message
    }).encode()
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=payload,
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
    )
    urllib.request.urlopen(req)


def run_crew_and_post(url: str, role: str, scraped_data: str):
    try:
        analyst_agent = Agent(
            role="Lead Competitive Intelligence Analyst",
            goal="Identify the primary value proposition, target audience, and product weaknesses from this scraped data.",
            backstory="You excel at reading marketing copy and finding the gaps, weaknesses, or customer pain points.",
            verbose=True,
            llm=gemini_llm
        )

        copywriter_agent = Agent(
            role="Senior Enterprise Sales Copywriter",
            goal="Create highly persuasive outreach text based on competitive vulnerabilities.",
            backstory="You convert complex competitive analysis into punchy, high-converting cold outreach sequences.",
            verbose=True,
            llm=gemini_llm
        )

        analysis_task = Task(
            description=f"Analyze this raw scraped website data:\n\n{scraped_data}\n\nExtract: 1. Core Value Prop, 2. Three likely product weaknesses or customer complaints.",
            expected_output="A structured markdown report detailing core value prop and 3 core weaknesses.",
            agent=analyst_agent
        )

        copywriting_task = Task(
            description=f"Review the analyst's report. Draft a single, hyper-targeted cold outreach email targeting a {role}. The email must position *our* generalized solutions directly against the competitor's 3 identified weaknesses without sounding overly aggressive.",
            expected_output="A ready-to-send markdown email template with Subject Line and Body.",
            agent=copywriter_agent
        )

        intelligence_crew = Crew(
            agents=[analyst_agent, copywriter_agent],
            tasks=[analysis_task, copywriting_task],
            process=Process.sequential
        )

        print(f"🚀 Kicking off deep analysis for: {url}")
        final_output = intelligence_crew.kickoff()

        post_to_slack(f"✅ *Analysis complete for {url}*\n\n{str(final_output)[:2900]}")

    except Exception as e:
        post_to_slack(f"❌ Analysis failed for `{url}`: {str(e)}")


@app.post("/api/analyze")
def run_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    url = request.competitor_url

    scraped_data = scrape_competitor_site(url)

    if "Failed to scrape" in scraped_data:
        post_to_slack(f"❌ Could not scrape `{url}`. Check the URL and try again.")
        return {"status": "scrape_failed"}

    # Kick off the crew in the background — returns instantly so Slack doesn't timeout
    background_tasks.add_task(run_crew_and_post, url, request.target_role, scraped_data)

    return {"status": "ok", "message": f"Analysis started for {url}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="::", port=8000)