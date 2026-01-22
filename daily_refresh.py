# daily_refresh.py

from app.db.database import SessionLocal
from app.services.sync_jobs import sync_all_sources


def refresh_jobs_and_vectors():
    db = SessionLocal()
    try:
        print("Starting daily sync_all_sources...")
        # IMPORTANT: just call sync_all_sources; it already rebuilds the vector store
        sync_all_sources(db)
        print("Daily sync completed.")
    finally:
        db.close()


if __name__ == "__main__":
    refresh_jobs_and_vectors()
