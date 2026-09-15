import os
import pandas as pd



def check_claim_history(customer_id: str) -> dict:
    """Return previous claims and summary for a customer."""
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CLAIMS_PATH = os.path.join(PROJECT_ROOT,"data","claims_history.csv")
    df = pd.read_csv(CLAIMS_PATH)
    customer_claims = df[df["customer_id"] == customer_id].copy()

    if customer_claims.empty:
        return {
            "customer_id": customer_id,
            "claim_count": 0,
            "previous_claims": []
        }

    customer_claims["claim_date"] = pd.to_datetime(customer_claims["claim_date"])
    customer_claims = customer_claims.sort_values("claim_date",ascending=False)

    return {
        "customer_id": customer_id,
        "claim_count": len(customer_claims),
        "previous_claims": customer_claims.to_dict(orient="records")
    }


if __name__ == "__main__":

    result = check_claim_history("C006")
    print(result)