import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from tools.claim_history import check_claim_history
from tools.fraud_risk import check_fraud_risk
from tools.policy_coverage import check_policy_coverage

mcp = FastMCP("Claims processing server")

@mcp.tool()
def policy_coverage(policy_id: str, claim_type: str, claim_amount: float) -> dict:
    """Check whether a claim type is covered by a policy"""
    print("SERVER: policy_coverage called", file=sys.stderr)
    result = "run policy-coverage mcp tool"
    result = check_policy_coverage(policy_id, claim_type, claim_amount)
    print("SERVER: policy_coverage finished", file=sys.stderr)
    return result

@mcp.tool()
def fraud_risk(customer_id: str, claim_amount: float) -> dict:
    """Assess the fraud risk of a claim based on the customer's claim history"""
    return check_fraud_risk(customer_id, claim_amount)


@mcp.tool()
def claim_history(customer_id: str) -> dict:
    """Retrieve the claim history for a customer"""
    return check_claim_history(customer_id)


if __name__ == "__main__":
    print("Starting MCP server...", file=sys.stderr)
    mcp.run()