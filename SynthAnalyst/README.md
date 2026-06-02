# SynthAnalyst
A multi-agent AI system built with CrewAI that autonomously researches global financial markets and synthesizes data into actionable investor briefs.
_______________________________________________________________________________________________________________________________________________________________________________________________________________

# Autonomous Market Analysis Crew

An automated, multi-agent AI system that tracks specific financial assets (NASDAQ futures, Bitcoin) and synthesizes the latest market sentiment into actionable briefs. 

This project demonstrates the orchestration of autonomous agents using **CrewAI**, leveraging sequential process flows and model-agnostic architecture. Currently configured to run on Google's **Gemini 2.5 Flash** for high-speed, cost-efficient inference.

---

## System Architecture

The workflow is managed by a sequential `Process`, ensuring strict data hand-offs between specialized agents to minimize hallucinations and maintain context.

| Agent | Role | Execution Goal |
| :--- | :--- | :--- |
| **Market Researcher** | Data Gathering & Sentiment | Pulls the latest breaking news on specified assets and distills the top headlines into a structured sentiment summary. |
| **Financial Analyst** | Synthesis & Reporting | Ingests the researcher's raw data to draft a concise, two-paragraph market brief forecasting impacts on the tech and crypto sectors. |

---

## Tech Stack

*   **Framework:** [CrewAI](https://www.crewai.com/)
*   **LLM Provider:** Google Gemini API (via CrewAI native `LLM` class)
*   **Environment Management:** `python-dotenv`
*   **Language:** Python 3.10+

---

## Quick Start

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/autonomous-market-analyzer.git](https://github.com/yourusername/autonomous-market-analyzer.git)
cd autonomous-market-analyzer
