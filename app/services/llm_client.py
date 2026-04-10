from llm_service.llm_server import generate_text

def call_llm(prompt: str, max_new_tokens: int = 256) -> str:
    print("\n[LLM] Prompt preview:\n", prompt[:400], "...\n")

    output = generate_text(prompt)

    print("[LLM] Output text preview:\n", output[:300], "...\n")
    return output