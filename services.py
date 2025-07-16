import requests, time, os
from dotenv import load_dotenv

load_dotenv()
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def upload_audio(file_path):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    with open(file_path, 'rb') as f:
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, files={'file': f})
    return response.json()['upload_url']

def transcribe_audio(audio_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": audio_url,
        "word_boost": [],
        "boost_param": "high",
        "iab_categories": False,
        "auto_chapters": False
    }
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    response = requests.post(endpoint, json=json, headers=headers)
    transcript_id = response.json()['id']

    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    while True:
        res = requests.get(polling_endpoint, headers=headers).json()
        if res['status'] == 'completed':
            return res
        elif res['status'] == 'error':
            raise Exception(res['error'])
        time.sleep(3)

def pronunciation_score(words):
    confidences = [w['confidence'] for w in words]
    avg_conf = sum(confidences) / len(confidences)
    mispronounced = [
        {"word": w['word'], "start": w['start'], "confidence": w['confidence']}
        for w in words if w['confidence'] < 0.85
    ]
    return {
        "pronunciation_score": int(avg_conf * 100),
        "mispronounced_words": mispronounced
    }

def pacing_eval(words, duration):
    wpm = (len(words) / duration) * 60
    if wpm < 90:
        feedback = "Too slow"
    elif wpm > 150:
        feedback = "Too fast"
    else:
        feedback = "Your speaking pace is appropriate."
    return {
        "pacing_wpm": round(wpm),
        "pacing_feedback": feedback
    }

def pause_detection(words):
    pause_count = 0
    total_pause = 0.0
    for i in range(1, len(words)):
        pause = words[i]['start'] - words[i - 1]['end']
        if pause > 0.5:
            pause_count += 1
            total_pause += pause
    feedback = "Try to reduce long pauses to improve fluency." if pause_count else "Good fluency with minimal pauses."
    return {
        "pause_count": pause_count,
        "total_pause_time_sec": round(total_pause, 2),
        "pause_feedback": feedback
    }

def generate_feedback(pacing, pronunciation, pause):
    feedback = []
    feedback.append(pacing["pacing_feedback"])
    if pronunciation["mispronounced_words"]:
        words = ', '.join([w["word"] for w in pronunciation["mispronounced_words"]])
        feedback.append(f"Focus on pronouncing {words} more clearly.")
    feedback.append(pause["pause_feedback"])
    return {"text_feedback": " ".join(feedback)}