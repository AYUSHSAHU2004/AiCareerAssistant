import json
from typing import List, Dict, Any
from app.services.llm_client import call_llm


def build_rerank_prompt(
    candidate_profile: str,
    job_title: str,
    job_description: str,
    job_location: str = ""
) -> str:
    return f"""
You are an ATS that evaluates how suitable a job is for a candidate.

Candidate profile:
\"\"\"{candidate_profile}\"\"\"

Job:
Title: {job_title}
Location: {job_location}
Description:
\"\"\"{job_description}\"\"\"

Task:
1. Consider:
   - Required years of experience.
   - Seniority (e.g., intern/junior/SDE1 vs SDE2/senior/staff).
   - Tech stack match.
   - Location fit (prefer roles in the same city/country or remote if the candidate can work remotely).
2. Decide how appropriate this job is for the candidate on a scale from 0 to 10, where:
   - 0 = totally inappropriate (e.g., requires 5+ years, senior/staff role for a student, or location impossible for the candidate).
   - 10 = extremely well matched (e.g., internship/entry-level software engineer role in a compatible location).

Respond ONLY in strict JSON like:
{{"score": <number between 0 and 10>, "reason": "<short explanation>"}}
""".strip()

def parse_score_from_llm_output(output: str) -> Dict[str, Any]:
    # Try to extract JSON block
    start = output.find("{")
    end = output.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_str = output[start : end + 1]
        try:
            obj = json.loads(json_str)
            score = float(obj.get("score", 0))
            reason = str(obj.get("reason", "")).strip()
            return {"score": score, "reason": reason}
        except Exception:
            pass
    return {"score": 0.0, "reason": "Failed to parse LLM output"}

def rerank_jobs_with_llm(raw_resume_text: str, docs, top_n: int = 10) -> List[Dict[str, Any]]:
    """
    docs: list[Document] from FAISS (page_content, metadata with job_id, title, etc.)
    """
    candidate_profile = raw_resume_text
    scored: List[Dict[str, Any]] = []
    for d in docs:
        job_title = d.metadata.get("title", "")
        job_description = d.page_content

        prompt = build_rerank_prompt(candidate_profile, job_title, job_description)
        output = call_llm(prompt, max_new_tokens=128)
        parsed = parse_score_from_llm_output(output)

        scored.append(
            {
                "job_id": d.metadata.get("job_id"),
                "doc": d,
                "score": parsed["score"],
                "reason": parsed["reason"],
            }
        )
    
    # Sort by score desc and filter low scores
    scored.sort(key=lambda x: x["score"], reverse=True)
    filtered = [s for s in scored if s["score"] >= 5.0]

    return filtered[:top_n]


