from app.services.llm_client import call_llm  # this should call your local LLM /generate


def build_referral_email_prompt(
    candidate_resume: str,
    job_title: str,
    job_description: str,
    employee_name: str,
    company_name: str,
) -> str:
    return f"""
You are an assistant that writes concise, professional referral request emails.

Candidate resume:
\"\"\"{candidate_resume}\"\"\"

Target job:
Title: {job_title}
Company: {company_name}
Description:
\"\"\"{job_description}\"\"\"

Recipient:
Name: {employee_name}
Role: Employee at {company_name}

Task:
Write a short, polite referral request email from the candidate to this employee.

Constraints:
- Start with a "Subject: ..." line.
- Then a blank line.
- Then the email body.
- Address the employee by name.
- Mention the specific job title and company.
- Briefly highlight 2–3 relevant strengths from the resume.
- Ask if they would be open to referring the candidate.
- Keep it 2–3 short paragraphs.
- Do NOT add any JSON or extra explanation, only the email text.
""".strip()


def generate_referral_email(
    candidate_resume: str,
    job_title: str,
    job_description: str,
    employee_name: str,
    company_name: str,
) -> str:
    prompt = build_referral_email_prompt(
        candidate_resume, job_title, job_description, employee_name, company_name
    )
    output = call_llm(prompt, max_new_tokens=256)
    return output.strip()

