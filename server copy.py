from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

#Initiate the flask app : TODO
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def sent_analyzer():
    # TODO
    text_to_analyze = request.args.get('textToAnalyze')
    emotion_result = emotion_detector(text_to_analyze)
    

    anger = emotion_result['anger']
    disgust = emotion_result['disgust']
    fear = emotion_result['fear']
    joy = emotion_result['joy']
    sadness = emotion_result['sadness']
    dominant_emotion = emotion_result['dominant_emotion']

    if dominant_emotion is None:
        return "Texto invalido! Intente nuevamente"

    response_str = (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return response_str 

@app.route("/")
def render_index_page():
    #TODO
    return render_template('index.html')

if __name__ == "__main__":
    '''#TODO
    app.run(host="0.0.0.0", port=5000)