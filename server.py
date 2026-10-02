"""
Emotion Detection Server

This module executes a Flask web server for the Emotion Detection application.
It provides endpoints to render the web interface and analyze emotions from user input text.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def sent_analyzer():
    """
    Analyzes the emotion of the input text provided via query parameters
    and returns a formatted string with emotion scores and the dominant emotion.
    Returns an error message if the input is blank or invalid.
    """
    try:
        text_to_analyze = request.args.get('textToAnalyze')
        
        # Error handling: check if text is provided and not empty
        if text_to_analyze is None or text_to_analyze.strip() == '':
            return "Invalid text! Please try again!"
        
        response = emotion_detector(text_to_analyze)

        # Error handling: check if emotion detection was successful
        if response['dominant_emotion'] is None:
            return "Invalid text! Please try again!"

        return (
            f"For the given statement, the system response is "
            f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
            f"'fear': {response['fear']}, 'joy': {response['joy']} and "
            f"'sadness': {response['sadness']}. "
            f"The dominant emotion is {response['dominant_emotion']}."
        )
    except Exception as e:
        print(f"ERROR: Unexpected error in sent_analyzer - {str(e)}")
        return "An error occurred while processing your request. Please try again."

@app.route("/")
def render_index_page():
    """
    Renders the main index page of the Emotion Detector application.
    """
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"ERROR: Failed to render index page - {str(e)}")
        return "Error loading the application. Please refresh the page.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
