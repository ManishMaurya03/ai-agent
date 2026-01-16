from mcp.server.fastmcp import FastMCP
from langfuse import observe
app = FastMCP("LoanApprovalMcpServer")

@app.tool()
@observe(name="evaluate_loan_tool")
def evaluate_loan(
    age: int,
    monthly_income: float,
    existing_emi: float,
    credit_score: int
) -> str:
    """
    Evaluate loan eligibility based on basic financial rules
    """

    # Rule 1: Age check
    if age < 21 or age > 60:
        return "REJECTED: Age not within eligible range"

    # Rule 2: Credit score
    if credit_score < 650:
        return "REJECTED: Low credit score"
            
        

    # Rule 3: EMI to income ratio
    emi_ratio = existing_emi / monthly_income
    if emi_ratio > 0.4:
        return "REJECTED: High EMI burden"


    # Eligible loan calculation
    eligible_amount = monthly_income * 60

    return f"APPROVED: Eligible for loan amount {eligible_amount}"

if __name__ == "__main__":
    app.run(transport="stdio")