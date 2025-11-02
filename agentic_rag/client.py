# client.py
import requests
import json
import argparse
import time
# replace this URL with your exposed URL from the API builder. The URL looks like this
SERVER_URL = 'http://0.0.0.0:3110'

def get_ideas(topic):
    query = f"""
        Give me 10 ideas for my English test base on the following topic: {topic}
        The idea should be innovate, unusual, and interesting to help the test takers not only improve their English skills but also learn something new about the world.
        After doing an English test with this idea, the test takers should also learn a comprehensive range of vocabularies related to the topic.
        Just show the ideas without any explantation and generatation guidance.
        Return the ideas in sentences seperated by |, for example:
        idea 1 | idea 2 | idea 3 | ... | idea 10
    """

    payload = {
        "query": query
    }
    try:
        response = requests.post(f"{SERVER_URL}/predict", json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        result = response.json()['output']['raw']
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None
