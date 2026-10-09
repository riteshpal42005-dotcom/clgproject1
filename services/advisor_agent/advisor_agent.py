# services/advisor_agent/advisor_agent.py

from agents import Agent

from services.llm import get_llm
from services.prompts import ADVISOR_AGENT_PROMPT

advisor_agent = Agent(
    name="Advisor Agent",
    instructions=ADVISOR_AGENT_PROMPT,
    model=get_llm(),
)