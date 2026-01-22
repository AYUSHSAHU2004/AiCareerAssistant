import requests

def call_llm(prompt: str, max_new_tokens: int = 256) -> str:
    print("\n[LLM] Prompt preview:\n", prompt[:400], "...\n")  # debug

    resp = requests.post(
        "http://localhost:9000/generate",
        json={"prompt": prompt, "max_new_tokens": max_new_tokens},
        timeout=120,
    )
    print("[LLM] Status:", resp.status_code)  # debug

    resp.raise_for_status()
    data = resp.json()
    print("[LLM] Raw response JSON:", data)  # debug

    output = data.get("output", "").strip()
    print("[LLM] Output text preview:\n", output[:300], "...\n")  # debug
    return output
