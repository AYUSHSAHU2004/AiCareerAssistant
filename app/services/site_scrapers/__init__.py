# app/services/site_scrapers/__init__.py
from app.services.site_scrapers.amazon_dom import AmazonDomScraper
from app.services.site_scrapers.base import BaseScraper


def get_scraper(scraper_type: str) -> BaseScraper:
    """
    Map scraper_type from JobSource to a concrete scraper class.
    """
    if scraper_type == "amazon_dom":
        return AmazonDomScraper()

    # add more mappings here for other sites
    raise ValueError(f"Unknown scraper_type: {scraper_type}")
