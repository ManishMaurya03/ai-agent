import os
from dotenv import load_dotenv
from langfuse.openai import OpenAI
from agents import Agent, function_tool,Runner
from langfuse import observe
# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# TOOLS (SIMULATED DATA SOURCES)
# -------------------------------

@function_tool
@observe()
def fetch_recent_logs(service_name: str) -> str:
    """
    Fetch recent error logs for a service.
    """
    return f"""
    ERROR  no data found at PaymentService get payment data()
    ERROR Timeout while calling Inventory API
    """


@function_tool
@observe()
def fetch_metrics(service_name: str) -> dict:
    """
    Fetch recent metrics for a service.
    """
    return {
        "cpu_usage": "92%",
        "memory_usage": "85%",
        "error_rate": "18%",
        "latency_p95": "4.2s"
    }


@function_tool
@observe()
def fetch_active_alerts(service_name: str) -> list:
    """
    Fetch active alerts for a service.
    """
    return [
        "High error rate alert",
        "Latency threshold breached"
    ]


# -------------------------------
# AGENT DEFINITION
# -------------------------------

incident_agent = Agent(
    name="IncidentTriageAgent",
    model="gpt-4o-mini", 
    instructions="""
    You are a senior SRE and incident commander.

    Your goal:
    - Understand the incident
    - Gather relevant data using tools
    - Identify the most likely root cause
    - Recommend immediate actions

    Be concise and structured.
    """,
    tools=[fetch_recent_logs, fetch_metrics, fetch_active_alerts],
)

# -------------------------------
# RUN AGENT
# -------------------------------


if __name__ == "__main__":
    service_name="payment-service"
    incident_summary="Users are unable to complete payments"
    result= Runner.run_sync(incident_agent,
        input=f"""
        Service: {service_name}
        Incident Summary: {incident_summary}

        Analyze and provide:
        1. Likely root cause
        2. Evidence
        3. Recommended actions
        """
        
    )
    print(result)