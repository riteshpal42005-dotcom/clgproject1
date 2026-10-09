# services/orchestrator.py

import asyncio

from agents import Agent, Runner, set_tracing_disabled

from services.llm import get_llm
from services.prompts import ORCHESTRATOR_PROMPT

from services.sales_agent.sales_agent import sales_agent
from services.inventory_agent.inventory_agent import inventory_agent
from services.advisor_agent.advisor_agent import advisor_agent

set_tracing_disabled(True)


business_orchestrator = Agent(
    name="Business Orchestrator",
    instructions=ORCHESTRATOR_PROMPT,
    model=get_llm(),
    handoffs=[
        sales_agent,
        inventory_agent,
        advisor_agent,
    ],
)


async def run_business_orchestrator(message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    result = await Runner.run(
        business_orchestrator,
        conversation_history + [
            {"role": "user", "content": message}
        ],
    )

    return result.final_output, result.to_input_list()


async def main():
    print("Business AI Assistant")
    print("Type 'exit' to quit.")

    conversation_history = []

    while True:
        message = input("\nYou: ").strip()

        if message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not message:
            continue

        try:
            response, conversation_history = (
                await run_business_orchestrator(
                    message,
                    conversation_history,
                )
            )

            print(f"\nAssistant: {response}")

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    asyncio.run(main())