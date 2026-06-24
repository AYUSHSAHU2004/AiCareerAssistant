from app.services.extract_video_id import extract_video_id
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import TranscriptsDisabled, YouTubeTranscriptApi

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)


def load_youtube_documents(youtube_url: str):
    video_id = extract_video_id(youtube_url)

    try:
        client = YouTubeTranscriptApi()
        transcript_list = client.fetch(video_id)

    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video")

    except Exception as e:
        raise ValueError(f"Failed to fetch YouTube transcript: {e}")

    # Combine entire transcript into one large text
    full_text = " ".join(item.text for item in transcript_list if item.text.strip())

    if not full_text.strip():
        raise ValueError("No transcript text found for this video")

    docs = [
        Document(
            page_content=full_text,
            metadata={
                "source": "youtube",
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
            },
        )
    ]

    return text_splitter.split_documents(docs)
