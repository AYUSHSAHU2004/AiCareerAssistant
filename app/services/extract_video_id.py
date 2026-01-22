from urllib.parse import urlparse, parse_qs

def extract_video_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    if "http" not in s and "youtu" not in s:
        return s
    parsed = urlparse(s)
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")
    if "youtube.com" in parsed.netloc:
        qs = parse_qs(parsed.query)
        vid = qs.get("v", [None])[0]
        if vid:
            return vid
    raise ValueError("Could not extract YouTube video id")
