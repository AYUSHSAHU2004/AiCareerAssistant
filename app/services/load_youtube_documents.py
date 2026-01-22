from app.services.extract_video_id import extract_video_id
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Assuming common splitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Define globally or pass as param

def load_youtube_documents(youtube_url: str):
    video_id = extract_video_id(youtube_url)
    try:
        client = YouTubeTranscriptApi()
        transcript_list = client.fetch(video_id)
    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video")
    except Exception as e:
        raise ValueError(f"Failed to fetch YouTube transcript: {e}")

    docs = []
    for item in transcript_list:
        start = item['start']  # Dict access, not attribute [web:11]
        text = item['text']
        if not text.strip():
            continue
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": "youtube",
                    "video_id": video_id,
                    "start": start,
                    "youtube_url": f"https://www.youtube.com/watch?v={video_id}&t={int(start)}s",
                },
            )
        )

    if not docs:
        raise ValueError("No transcript text found for this video")

    return text_splitter.split_documents(docs)
