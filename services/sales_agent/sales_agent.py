# services/sales_agent/sales_agent.py

from agents import Agent

from services.llm import get_llm
from services.prompts import SALES_AGENT_PROMPT

sales_agent = Agent(
    name="Sales Analytics Agent",
    instructions=SALES_AGENT_PROMPT,
    model=get_llm(),
)
