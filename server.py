from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

def _normalize_result(emotion_result: dict) -> dict:
    if all(k in emotion_result for k in ("anger", "disgust", "fear", "joy", "sadness")):
        result = {
            "anger":   float(emotion_result.get("anger", 0.0)),
            "disgust": float(emotion_result.get("disgust", 0.0)),
            "fear":    float(emotion_result.get("fear", 0.0)),
            "joy":     float(emotion_result.get("joy", 0.0)),
            "sadness": float(emotion_result.get("sadness", 0.0)),
        }

        dom = emotion_result.get("dominant_emotion")
        if not dom:
            dom = max(result, key=result.get) if any(result.values()) else None
        result["dominant_emotion"] = dom
        return result

    if "label" in emotion_result and "score" in emotion_result:
        base = {"anger": 0.0, "disgust": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.0}
        label = str(emotion_result["label"])
        score = float(emotion_result["score"])
        if label in base:
            base[label] = score
        base["dominant_emotion"] = label
        return base

    return {"anger": 0.0, "disgust": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.0, "dominant_emotion": None}

@app.route("/emotionDetector")
def emotion_analyzer():
    text_to_analyse = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyse:
        return "Invalid text! Please try again", 400

    try:
        raw = emotion_detector(text_to_analyse)
    except Exception as e:
        return f"Service error: {e}", 502

    result = _normalize_result(raw)
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again", 400

    anger   = result["anger"]
    disgust = result["disgust"]
    fear    = result["fear"]
    joy     = result["joy"]
    sadness = result["sadness"]
    dom     = result["dominant_emotion"]

    response_str = (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. The dominant emotion is {dom}."
    )
    return response_str

@app.route("/")
def render_index_page():
    return render_template("index.html")

if __name__ == "__main__":
    # Despliegue en localhost:5000 como pide la tarea
    app.run(host="0.0.0.0", port=5000)
