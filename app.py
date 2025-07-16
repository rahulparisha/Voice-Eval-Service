from fastapi import FastAPI, UploadFile, File
from utils.transcriber import transcribe_audio
from utils.analyzer import analyze_pronunciation, evaluate_pacing, detect_pauses
from utils.feedback import generate_feedback

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    result = await transcribe_audio(file)
    return result

@app.post("/evaluate")
async def evaluate(file: UploadFile = File(...)):
    transcript_data = await transcribe_audio(file)

    pronunciation_result = analyze_pronunciation(transcript_data["words"])
    pacing_result = evaluate_pacing(transcript_data["words"], transcript_data["audio_duration_sec"])
    pause_result = detect_pauses(transcript_data["words"])
    text_feedback = generate_feedback(pronunciation_result, pacing_result, pause_result)

    return {
        "transcription": transcript_data,
        "pronunciation": pronunciation_result,
        "pacing": pacing_result,
        "pauses": pause_result,
        "text_feedback": {"text_feedback": text_feedback}
    }