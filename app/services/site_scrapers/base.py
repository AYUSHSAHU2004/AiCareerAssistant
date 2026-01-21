# app/services/site_scrapers/base.py
from abc import ABC, abstractmethod
from typing import List
from app.services.job_schema import JobDict
from app.db import models


class BaseScraper(ABC):
    @abstractmethod
    def scrape(self, source: models.JobSource) -> List[JobDict]:
        """
        Given a JobSource row, fetch jobs and return a list of JobDict.
        """
        ...
