import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
VECTOR_DB_PATH = os.path.join(PROJECT_ROOT,"data","faiss_index")
import sys
print("RETRIEVER: loading embeddings...", file=sys.stderr, flush=True)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("RETRIEVER: loading FAISS index...", file=sys.stderr, flush=True)
vector_db = FAISS.load_local(VECTOR_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
print("RETRIEVER: ready", file=sys.stderr, flush=True)


# Search policy documents
def search_policy(query, policy_id=None, k=4):
    # Paths
    if policy_id:
        # Retrieve more candidates first, then filter
        results = vector_db.similarity_search(query,k=20)

        results = [doc for doc in results if doc.metadata.get("policy_id") == policy_id]
        return results[:k]

    return vector_db.similarity_search(query,k=k)



# Run the file
if __name__ == "__main__":
    query = "Does this policy cover accidental vehicle damage?"

    results = search_policy(query=query,policy_id="P001")

    for i, doc in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")
        print(f"Policy ID: {doc.metadata.get('policy_id')}")
        print(f"Source: {doc.metadata.get('source')}")
        print(doc.page_content)