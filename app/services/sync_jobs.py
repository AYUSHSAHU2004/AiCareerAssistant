from sqlalchemy.orm import Session
from app.db import models
from app.db.crud_jobs import upsert_jobs_for_source
from app.services.site_scrapers import get_scraper
from app.services.vector_store import rebuild_vector_store


def sync_all_sources(db: Session) -> None:
    sources = (
        db.query(models.JobSource)
        .filter(models.JobSource.enabled == True)
        .all()
    )

    for source in sources:
        scraper = get_scraper(source.scraper_type)
        jobs = scraper.scrape(source)
        upsert_jobs_for_source(db, source, jobs)
    
    
    rebuild_vector_store(db)
