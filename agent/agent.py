import os
import asyncio
import sys
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

# Customer C006 has submitted a claim of
# Rs. 180000 for accidental damage under policy P006.
# Evaluate this claim.

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL_ID = "openai/gpt-oss-20b"


async def main():
    # 1. Connect to MCP server
    client = MultiServerMCPClient(
        {
            "claims_server": {
                "command": sys.executable,
                "args": [
                    "mcp_server/server.py"
                ],
                "transport": "stdio",
            }
        }
    )

    # 2. Get MCP tools
    tools = await client.get_tools()
    print("Available MCP tools:")
    for tool in tools:
        print("-", tool.name)

    print("loading llm....")
    # 3. Create Groq LLM
    llm = ChatGroq(model=GROQ_MODEL_ID,temperature=0,groq_api_key=GROQ_API_KEY)
    print("llm loaded\nCreating agent...")
    # 4. Create Agent
    agent = create_agent(model=llm,tools=tools,
                        system_prompt = 
                        """
                        You are an insurance claims processing agent.
                        For every claim evaluation:
                        1. Use policy_coverage to verify whether the claim is covered.
                        2. Use claim_history to retrieve the customer's previous claims.
                        3. Use fraud_risk to assess the fraud risk.

                        Do not invent information.
                        After gathering the required evidence, provide:

                        1. Policy Coverage Assessment
                        2. Claim History Summary
                        3. Fraud Risk Assessment
                        4. Final Recommendation: APPROVE, REJECT, or REFER
                        5. Brief Reason

                        A final recommendation is not a final claim decision.
                        Human claims handler review is required.
                        """
    )

    print("Agent created!\nInvoking agent")
    # 5. Run agent
    import time
    start_time = time.time()
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
    Evaluate this insurance claim:
    Customer ID: C006
    Policy ID: P006
    Claim Type: Accidental damage
    Claim Amount: Rs. 180000
    Check the policy coverage, claim history, and fraud risk.
    Then provide a final recommendation.
    """
                }
            ]
        }
    )
    print("Agent invocation complete!")
    # 6. Print final response
    print("\nFinal Agent Response:\n")
    print(result["messages"][-1].content)

    print("Agent took '",time.time() - start_time, "' seconds to complete agent invocation")

if __name__ == "__main__":
    asyncio.run(main())