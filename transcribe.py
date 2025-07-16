import httpx
import tempfile
import shutil
import os

ASSEMBLYAI_API_KEY="d59ef12e45b44d8aaae068f0446dccdf"

async def transcribe_audio(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    # Upload audio
    with open(temp_path, 'rb') as f:
        upload_response = httpx.post(
            "https://api.assemblyai.com/v2/upload",
            headers={"authorization": ASSEMBLYAI_API_KEY},
            content=f.read()
        )
        audio_url = upload_response.json()["upload_url"]

    # Transcribe
    transcript_response = httpx.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url, "punctuate": True, "format_text": True, "word_boost": []}
    )
    transcript_id = transcript_response.json()["id"]

    # Polling
    while True:
        poll_response = httpx.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        result = poll_response.json()
        if result["status"] == "completed":
            break
        elif result["status"] == "error":
            raise Exception(f"Transcription failed: {result['error']}")

    os.remove(temp_path)

    words = [{
        "word": w["text"],
        "start": w["start"] / 1000,
        "end": w["end"] / 1000,
        "confidence": w["confidence"]
    } for w in result["words"]]

    return {
        "transcript": result["text"],
        "words": words,
        "audio_duration_sec": result["audio_duration"] / 1000
    }