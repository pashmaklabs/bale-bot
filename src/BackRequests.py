import os, requests
from dotenv import find_dotenv, load_dotenv

# Getting environment variables

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

SERVER_BASE_URL = os.getenv("SERVER_BASE_URL")

# Backend requests

def get_place_comments(place_id: int) -> list:
    api_response = requests.get(f"{SERVER_BASE_URL}/comments/{str(place_id)}")

    comments = []

    if api_response.status_code == 200:
        response = api_response.json()
        comments = response['comments']

    return comments

def get_places(search_term: str) -> list:
    api_response = requests.get(f"{SERVER_BASE_URL}/places/?q={search_term}")

    places = []

    if api_response.status_code == 200:
        response = api_response.json()
        places = response['places']

    return places

if __name__ == "__main__":
    comments = get_place_comments(455994176)
    print(comments)