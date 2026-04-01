from typing import List, Dict
from bs4 import BeautifulSoup
from app.services.playwright_client import render_page_html_sync


 def scrape_job_source_url(url: str) -> List[Dict[str, str]]:
    """
    Scrape Amazon jobs page with Playwright and extract job details.
    """
    html = render_page_html_sync(url, wait_selector=None)
    soup = BeautifulSoup(html, "html.parser")

    # DEBUG: Check if we're getting HTML
    print(f"[DEBUG] HTML length: {len(html)}")
    print(f"[DEBUG] First 500 chars: {html[:500]}")

    jobs: List[Dict[str, str]] = []

    # Find all job cards
    job_cards = soup.select("div.job-tile")
    print(f"[DEBUG] Found {len(job_cards)} job cards with selector 'div.job-tile'")

    # If no cards found, try alternate selectors
    if not job_cards:
        print("[DEBUG] Trying alternate selector 'div.job'")
        job_cards = soup.select("div.job")
        print(f"[DEBUG] Found {len(job_cards)} with 'div.job'")

    for idx, card in enumerate(job_cards):
        print(f"[DEBUG] Processing card {idx}")
        job_data = {}

        # Try to extract title
        title_el = card.select_one("h3.job-title a.job-link")
        if not title_el:
            print(f"[DEBUG] Card {idx}: No title found with 'h3.job-title a.job-link'")
            # Try simpler selector
            title_el = card.select_one("a")
        
        job_data["title"] = title_el.get_text(strip=True) if title_el else "N/A"
        print(f"[DEBUG] Card {idx} title: {job_data['title']}")

        # Rest of extraction...
        job_data["link"] = title_el["href"] if title_el and title_el.has_attr("href") else "N/A"

        job_inner = card.select_one("div.job")
        job_data["job_id"] = job_inner.get("data-job-id", "N/A") if job_inner else "N/A"

        location_el = card.select_one("div.location-and-id .text-nowrap")
        job_data["location"] = location_el.get_text(strip=True) if location_el else "N/A"

        date_el = card.select_one("span.posting-date")
        job_data["posted_date"] = date_el.get_text(strip=True) if date_el else "N/A"

        updated_el = card.select_one("p.meta.time-elapsed")
        job_data["last_updated"] = updated_el.get_text(strip=True) if updated_el else "N/A"

        qualifications_div = card.select_one("div.qualifications-preview")
        if qualifications_div:
            qual_items = qualifications_div.select("li")
            job_data["qualifications"] = " | ".join(
                [li.get_text(strip=True) for li in qual_items]
            ) if qual_items else "N/A"
        else:
            job_data["qualifications"] = "N/A"

        read_more_el = card.select_one("a.read-more")
        job_data["read_more_link"] = read_more_el["href"] if read_more_el and read_more_el.has_attr("href") else job_data["link"]

        if job_data["title"] != "N/A":
            jobs.append(job_data)

    print(f"[DEBUG] Total jobs extracted: {len(jobs)}")
    return jobs
