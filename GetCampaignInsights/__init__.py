import os
import json
import logging
import azure.functions as func

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.ai.inference import ChatCompletionsClient


def _env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise ValueError(f"Missing env var: {name}")
    return v

def _search_docs(query: str, top_k: int = 5):
    search = SearchClient(
        endpoint=_env("AZURE_SEARCH_ENDPOINT"),
        index_name=_env("AZURE_SEARCH_INDEX"),
        credential=AzureKeyCredential(_env("AZURE_SEARCH_API_KEY")),
    )

    results = search.search(
        search_text=query or "*",
        top=top_k
    )

    docs = []
    for r in results:
        d = dict(r)
        docs.append({
            "title": d.get("metadata_storage_name") or d.get("id"),
            "content": d.get("content"),
            "source": d.get("metadata_storage_name"),
            "url": None
        })

    return docs



def _build_prompt(question: str, docs):
    parts = []
    for i, d in enumerate(docs, start=1):
        title = d.get("title") or f"Doc {i}"
        src = d.get("url") or d.get("source") or "unknown"
        content = (d.get("content") or "").strip()
        if len(content) > 1200:
            content = content[:1200] + "…"
        parts.append(f"[{i}] {title} ({src})\n{content}")

    sources = "\n\n".join(parts) if parts else "No sources found."

    return f"""
You are a campaign insights assistant. Use ONLY the sources provided.

Question:
{question}

Sources:
{sources}

Return JSON only:
{{
  "summary": string,
  "keyPoints": [string],
  "recommendations": [string]
}}
""".strip()


def _foundry_chat(prompt: str):
    client = ChatCompletionsClient(
        endpoint=_env("AZURE_INFERENCE_ENDPOINT").rstrip("/"),
        credential=AzureKeyCredential(_env("AZURE_INFERENCE_KEY")),
        model=_env("AZURE_INFERENCE_MODEL"),
        api_version=os.getenv("AZURE_INFERENCE_API_VERSION", "2024-05-01-preview")
    )

    resp = client.complete(
        messages=[
            {"role": "system", "content": "Be strict: only use provided sources."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return resp.choices[0].message.content or "{}"


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        question = req.params.get("q") or "What is the budget allocation for the Q3 Summer campaign?"
        

        docs = _search_docs(question, top_k=5)
        prompt = _build_prompt(question, docs)
        raw = _foundry_chat(prompt)

        try:
            rag = json.loads(raw)
        except json.JSONDecodeError:
            rag = {"summary": raw, "keyPoints": [], "recommendations": []}

        citations = []
        for i, d in enumerate(docs, start=1):
            citations.append({
                "id": i,
                "title": d.get("title") or f"Doc {i}",
                "source": d.get("url") or d.get("source") or "unknown"
            })

        return func.HttpResponse(
            json.dumps({               
                "question": question,
                "rag": rag,
                "citations": citations
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as ex:
        logging.exception("GetCampaignInsights failed")
        return func.HttpResponse(
            json.dumps({"error": str(ex)}),
            status_code=500,
            mimetype="application/json"
        )
