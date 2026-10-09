# services/inventory_agent/inventory_agent.py

from agents import Agent
from tools.inventory_tools import (
    get_all_products,
    get_low_stock_products,
)
from services.llm import get_llm
from services.prompts import INVENTORY_AGENT_PROMPT

inventory_agent = Agent(
    name="Inventory Agent",
    instructions=INVENTORY_AGENT_PROMPT,
    model=get_llm(),
    tools=[
        get_all_products,
        get_low_stock_products,
    ]
)