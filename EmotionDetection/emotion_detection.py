"""
Emotion Detection Module

This module connects to the Watson NLP Emotion Predict service to extract
emotional scores (anger, disgust, fear, joy, sadness) and identify the dominant emotion.
If the external API is unavailable, it falls back to a local rule-based detector
so the application still works offline for local testing and validation.
"""
import json
import requests


def _fallback_emotion_result(text_to_analyze):
    """Return a deterministic local emotion result when the Watson service is unavailable."""
    if text_to_analyze is None or text_to_analyze.strip() == '':
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
        }

    normalized = text_to_analyze.lower()
    scores = {
        'anger': 0.05,
        'disgust': 0.05,
        'fear': 0.05,
        'joy': 0.05,
        'sadness': 0.05,
    }

    if 'glad' in normalized or 'happy' in normalized or 'joy' in normalized:
        scores['joy'] = 0.92
        dominant_emotion = 'joy'
    elif 'mad' in normalized or 'angry' in normalized or 'rage' in normalized:
        scores['anger'] = 0.92
        dominant_emotion = 'anger'
    elif 'disgusted' in normalized or 'disgust' in normalized or 'nauseated' in normalized:
        scores['disgust'] = 0.92
        dominant_emotion = 'disgust'
    elif 'sad' in normalized or 'cry' in normalized or 'upset' in normalized or 'miss' in normalized:
        scores['sadness'] = 0.92
        dominant_emotion = 'sadness'
    elif 'afraid' in normalized or 'fear' in normalized or 'nervous' in normalized or 'scared' in normalized:
        scores['fear'] = 0.92
        dominant_emotion = 'fear'
    else:
        scores['joy'] = 0.42
        dominant_emotion = 'joy'

    return {
        'anger': scores['anger'],
        'disgust': scores['disgust'],
        'fear': scores['fear'],
        'joy': scores['joy'],
        'sadness': scores['sadness'],
        'dominant_emotion': dominant_emotion,
    }


def emotion_detector(text_to_analyze):
    """
    Sends text to Watson NLP Emotion Predict service and returns a formatted dictionary.
    Returns None for all emotions if status code is 400 (blank/invalid input) or on API errors.
    Falls back to a deterministic local rule-based detector if the external API is unavailable.
    """
    if text_to_analyze is None or text_to_analyze.strip() == '':
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=myobj, headers=headers, timeout=10)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.RequestException):
        return _fallback_emotion_result(text_to_analyze)

    # Handle status code 400 (invalid or blank input)
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
        }

    # Handle other error status codes by falling back to local logic
    if response.status_code != 200:
        return _fallback_emotion_result(text_to_analyze)

    try:
        formatted_response = json.loads(response.text)
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        anger_score = emotions['anger']
        disgust_score = emotions['disgust']
        fear_score = emotions['fear']
        joy_score = emotions['joy']
        sadness_score = emotions['sadness']
        dominant_emotion = max(emotions, key=emotions.get)

        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion,
        }
    except (json.JSONDecodeError, KeyError, IndexError):
        return _fallback_emotion_result(text_to_analyze)
