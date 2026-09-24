# Final Project - Emotion Detection Application

Welcome to the **Emotion Detection Application** built using Python, Watson NLP, and Flask.

## Project Description
This web application analyzes user-provided text to evaluate emotional tone. Using IBM Watson's NLP Emotion Predict library, the system processes input statements and calculates emotion confidence scores across five categories:
- **Anger**
- **Disgust**
- **Fear**
- **Joy**
- **Sadness**

The application also calculates and reports the **Dominant Emotion** for the input text and handles invalid or blank inputs gracefully.

## Project Structure
- `EmotionDetection/`: Package containing the emotion detection module.
  - `__init__.py`: Package initialization file exposing `emotion_detector`.
  - `emotion_detection.py`: Core function interacting with the Watson NLP service.
- `server.py`: Flask web server with routing, UI rendering, and error handling.
- `test_emotion_detection.py`: Unit test suite testing 5 core emotional statements.
- `templates/index.html`: Web interface front-end.
- `static/mywebscript.js`: Client-side script handling AJAX requests to the server.
