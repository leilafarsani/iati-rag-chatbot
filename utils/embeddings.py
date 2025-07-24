from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(docs, user_question):
    texts = []
    for doc in docs:
        title = doc.get("title_narrative", [""])[0]
        desc = doc.get("description_narrative", [""])[0] if doc.get("description_narrative") else ""
        texts.append(f"{title}: {desc}")

    if not texts:
        return ""

    embeddings = model.encode(texts)
    query_embedding = model.encode([user_question])[0]

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))
    D, I = index.search(np.array([query_embedding]).astype("float32"), k=3)

    top_chunks = [texts[i] for i in I[0]]
    return "\n\n".join(top_chunks)
