from agents import Agent, Runner,model_settings,function_tool
import os
from dotenv import load_dotenv
from langfuse.openai import OpenAI


# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

agent = Agent(name="Assistant", 
              model="gpt-5-mini",
              instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write 1 page technical content about memory in agentic application max 300 character")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.