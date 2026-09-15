import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.retriever import search_policy


def check_policy_coverage(policy_id: str,claim_type: str,claim_amount: float) -> dict:
    """
    Check whether a claim type is covered by a policy
    and whether the claim amount is within the policy limit.
    """

    query = f"""
    Policy {policy_id}
    Claim type: {claim_type}
    Claim amount: Rs. {claim_amount}

    Is this claim type covered?
    What is the coverage limit?
    What exclusions or claim requirements apply?
    """

    print(f"Invoking policy_coverage tool for policy_id: {policy_id}\nclaim_type: {claim_type}\nclaim amount: {claim_amount}")
    print("llm response received")
    results = search_policy(query=query,policy_id=policy_id,k=4)

    print("/n Received search_policy results")
    if not results:
        return {
            "policy_id": policy_id,
            "covered": None,
            "within_limit": None,
            "coverage_limit": None,
            "evidence": [],
            "message": "No relevant policy evidence found."
        }

    evidence = []

    for doc in results:
        evidence.append({
            "source": doc.metadata.get("source"),
            "content": doc.page_content
        })

    return {
        "policy_id": policy_id,
        "claim_type": claim_type,
        "claim_amount": claim_amount,
        "evidence": evidence
    }


if __name__ == "__main__":

    result = check_policy_coverage(
        policy_id="P001",
        claim_type="Accidental damage",
        claim_amount=80000
    )

    print(result)