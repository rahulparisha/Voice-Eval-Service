def generate_feedback(pronunciation, pacing, pauses):
    feedback = []

    feedback.append(pacing["pacing_feedback"])
    
    if pronunciation["mispronounced_words"]:
        words = ', '.join([w["word"] for w in pronunciation["mispronounced_words"]])
        feedback.append(f"Focus on pronouncing '{words}' more clearly.")

    feedback.append(pauses["pause_feedback"])

    return " ".join(feedback)