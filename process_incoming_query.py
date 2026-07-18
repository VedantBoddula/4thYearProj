import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

LLM_MODEL = "llama3.1:8b"
OLLAMA_EMBEDDING_MODEL = "bge-m3"


def seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": OLLAMA_EMBEDDING_MODEL,
            "input": text_list
        }
    )
    return r.json()["embeddings"]


def inference(prompt):
    print("Thinking....")
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return r.json()["response"]


df = joblib.load("embeddings.joblib")

incoming_query = input("Ask a Question: ")

question_embedding = create_embedding([incoming_query])[0]

similarities = cosine_similarity(
    np.vstack(df["embedding"]),
    [question_embedding]
).flatten()

top_results = 7

max_index = similarities.argsort()[::-1][:top_results]

new_df = df.loc[max_index].copy()

# Add similarity score
new_df["score"] = similarities[max_index]

# Remove weak matches (optional)
new_df = new_df[new_df["score"] > 0.40]

# Keep only the best 2 chunks from each video
new_df = (
    new_df.sort_values("score", ascending=False)
          .groupby("number")
          .head(2)
)

# Convert timestamps to MM:SS
new_df["start"] = new_df["start"].apply(seconds_to_mmss)
new_df["end"] = new_df["end"].apply(seconds_to_mmss)

# print("\nRetrieved Chunks:\n")
# print(new_df[["number","title","start","end","text"]].to_string())

prompt = f"""
You are an AI tutor for the Sigma Web Development Course.

Below are the retrieved course sections that are most relevant to the user's question.

{new_df[["number","title","start","end","text"]].to_json(orient="records", indent=2)}

------------------------------------------------------------

User Question:
{incoming_query}

Instructions:

- Answer ONLY using the retrieved course sections above.
- Do NOT use outside knowledge.
- Do NOT guess or invent information.
- The timestamps are already correct. Use them exactly as provided.
- If multiple retrieved sections belong to the same video and discuss the same topic, combine them into a single answer.
- Mention only the videos that are actually relevant to the user's question.
- Write a short, natural summary (1-2 sentences) explaining what is taught in that section.
- Do NOT copy the subtitles word-for-word unless necessary.
- Do NOT mention JSON, subtitles, embeddings, chunks, retrieval, cosine similarity, or any internal process.
- If at least one relevant section is found, DO NOT say "I couldn't find this information."
- Reply with "I couldn't find this information in the available course." ONLY if none of the retrieved sections answer the question.

Return your answer in exactly this format:

Video Number: <number>
Video Title: <title>
Time: <start> - <end>
Summary: <Brief explanation>

<leave one blank line>

Video Number: <number>
Video Title: <title>
Time: <start> - <end>
Summary: <Brief explanation>

<leave one blank line if another video exists>
"""

with open("prompt.txt","w",encoding="utf-8") as f:
    f.write(prompt)

response = inference(prompt)

print("\nAnswer:\n")
print(response)

with open("response.txt","w",encoding="utf-8") as f:
    f.write(response)