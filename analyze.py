def analyze_pronunciation(words, threshold=0.85):
    total_conf = sum(w["confidence"] for w in words)
    avg_conf = total_conf / len(words) if words else 0
    mispronounced = [
        {"word": w["word"], "start": w["start"], "confidence": w["confidence"]}
        for w in words if w["confidence"] < threshold
    ]
    return {
        "pronunciation_score": int(avg_conf * 100),
        "mispronounced_words": mispronounced
    }

def evaluate_pacing(words, duration_sec):
    wpm = (len(words) / duration_sec) * 60 if duration_sec > 0 else 0
    if wpm < 90:
        feedback = "Too slow"
    elif wpm > 150:
        feedback = "Too fast"
    else:
        feedback = "Your speaking pace is appropriate."
    return {"pacing_wpm": int(wpm), "pacing_feedback": feedback}

def detect_pauses(words):
    pauses = []
    for i in range(1, len(words)):
        gap = words[i]["start"] - words[i - 1]["end"]
        if gap > 0.5:
            pauses.append(gap)
    return {
        "pause_count": len(pauses),
        "total_pause_time_sec": round(sum(pauses), 2),
        "pause_feedback": "Try to reduce long pauses to improve fluency." if len(pauses) > 2 else "Good fluency with minor pauses."
    }