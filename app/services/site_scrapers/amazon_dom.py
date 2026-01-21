from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.services.job_schema import JobDict
from app.services.site_scrapers.base import BaseScraper
from app.services.playwright_client import render_page_html_sync
from app.db import models


class AmazonDomScraper(BaseScraper):
    def scrape(self, source: models.JobSource) -> List[JobDict]:
        url = source.base_url
        html = render_page_html_sync(url, wait_selector="div.job-tile")

        soup = BeautifulSoup(html, "html.parser")
        job_cards = soup.select("div.job-tile")

        jobs: List[JobDict] = []

        for card in job_cards:
            job_div = card.select_one("div.job")
            external_job_id = job_div.get("data-job-id") if job_div else None
            if not external_job_id:
                continue

            title_el = card.select_one("h3.job-title a.job-link")
            title = title_el.get_text(strip=True) if title_el else None
            if not title:
                continue

            href = title_el["href"] if title_el and title_el.has_attr("href") else ""
            link = urljoin(url, href)

            location_el = card.select_one("div.location-and-id .text-nowrap")
            location = location_el.get_text(strip=True) if location_el else None

            # Description: join bullet points from qualifications-preview
            qualifications_div = card.select_one("div.qualifications-preview")
            description = None
            if qualifications_div:
                bullets = [li.get_text(strip=True) for li in qualifications_div.select("li")]
                description = "\n".join(bullets) if bullets else None

            job: JobDict = {
                "source_id": source.id,
                "external_job_id": external_job_id,
                "title": title,
                "company": "Amazon",
                "location": location,
                "link": link,
                "posted_date": None,   # can be parsed later from posting-date span
                "description": description,
                "raw_data": {},        # can stash extra fields here later
            }

            jobs.append(job)

        return jobs
