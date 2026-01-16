from langfuse.openai import OpenAI
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import os
import asyncio
from langfuse import observe
from dotenv import load_dotenv
from billing_prompt import  BILLING_AGENT_SYSTEM_PROMPT
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@observe(name="Billing-MCP-Server")
async def main():
    async with MCPServerStdio(
    name="billing_mcp",
    params={
        "command": "python3",
        "args": ["/Users/manishmaurya/Desktop/OpenAIApplications/FirstOpenAIProject/src/billing_agent/mcp_servers/billing_mcp_server.py"]
    }
) as billing_mcp:
        data_agent = Agent(
        name="DataAgent",
        model="gpt-4o-mini",
        instructions="Fetch customer and transaction data using MCP tools.",
        mcp_servers=[billing_mcp],
        )

        invoice_agent = Agent(
        name="InvoiceAgent",
        model="gpt-4o-mini",
        instructions="Generate structured invoice data and request PDF generation.",
        mcp_servers=[billing_mcp],
        )
        validation_agent = Agent(
        name="ValidationAgent",
        model="gpt-4o-mini",
        instructions="Validate billing details, taxes, and totals. Flag issues.",
       )
        payment_agent = Agent(
        name="PaymentAgent",
        model="gpt-4o-mini",
        instructions="Check payment status and decide next action.",
        mcp_servers=[billing_mcp],
        )
        reminder_agent = Agent(
        name="ReminderAgent",
        model="gpt-4o-mini",
        instructions="Send reminders for overdue invoices.",
        mcp_servers=[billing_mcp],
      )
        
        orchestrator = Agent(
            name="BillingOrchestrator",
            model="gpt-4o-mini",
            instructions=BILLING_AGENT_SYSTEM_PROMPT,
            handoffs=[data_agent, invoice_agent, validation_agent, payment_agent, reminder_agent],
            mcp_servers=[billing_mcp],
        )

        result = await Runner.run(
            orchestrator,
            input="Process billing for customer CUST-101",
        )

        print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main())