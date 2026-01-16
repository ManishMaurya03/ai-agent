from langfuse.openai import OpenAI
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from config import OPENAI_API_KEY
import os
import asyncio
from langfuse import observe


client = OpenAI(api_key=OPENAI_API_KEY)
@observe(name="loan_approval_agent")
async def main():
    async with MCPServerStdio(
    name="loan_mcp",
    params={
        "command": "python3",
        "args": ["loan_mcp_server.py"]
    }
) as loan_mcp:

        agent = Agent(
        name="LoanAdvisorAgent",
        model="gpt-5-mini",
        instructions="""
        You are a loan advisor.
        Always use the loan evaluation tool.
        Explain approval or rejection clearly. answer only question related to loan approval. 
        if question is not related to loan approval then answer "I can only answer questions related to loan approval."
        """,
        mcp_servers=[loan_mcp]
)

        result = await Runner.run(
            agent,
            "Applicant age 30, income 100000, EMI 15000, credit score 720. Will the loan be approved?",
        )

        print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main())