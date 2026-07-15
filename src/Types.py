from src.BackRequests import (
    get_place_comments,
    get_places,
)

# Classes

class Place:
    def __init__(self, place_data: dict):
        if place_data["osm_id"]:
            self.osm_id: int = place_data["osm_id"]
        else:
            self.osm_id: int = place_data["id"]

        self.name: str = place_data["name"]
        self.latitude: float = round(place_data["latitude"], 7)
        self.longitude: float = round(place_data["longitude"], 7)
        self.image_urls: list[str] = place_data["image_urls"]
        self.rating: int = place_data["rating"]
        self.comments: list[Comment] = self.get_comments()

    def __str__(self):
        return f"{self.name}\nامتیاز کاربران: {self.rating}"

    def get_comments(self) -> list:
        comments_data = get_place_comments(self.osm_id)

        comments = [Comment(c) for c in comments_data]

        return comments

    def get_first_image_url(self):
        if self.image_urls:
            return self.image_urls[0]
        return None

    @classmethod
    def get_places(self, search_term: str):
        places_data = get_places(search_term)

        places = [Place(p) for p in places_data]
            
        return places


class Comment:
    def __init__(self, comment_data: dict):
        self.content: str = comment_data["content"]
        self.rating: int = comment_data["rating"]
        self.user_lastname: str = comment_data["user"]["first_name"]
        self.user_firstname: str = comment_data["user"]["last_name"]
        self.likes: int = comment_data["likes"]
        self.dislikes: int = comment_data["dislikes"]

    def __repr__(self):
        return f"ثبت شده توسط کاربر {self.get_sender_fullname()}\nامتیاز کاربر: {self.rating}\nمتن نظر: {self.content}\nتعداد لایک: {self.likes}\nتعداد دیسلاک: {self.dislikes}"
    
    def __str__(self):
        return f"ثبت شده توسط کاربر {self.get_sender_fullname()}\nامتیاز کاربر: {self.rating}\nمتن نظر: {self.content}\nتعداد لایک: {self.likes}\nتعداد دیسلاک: {self.dislikes}"

    def get_sender_fullname(self):
        return f"{self.user_firstname.strip()} {self.user_lastname.strip()}"


class SearchResult:
    def __init__(self, current_place: Place, places: list[Place]):
        self.current_place = current_place
        self.places = places


# import json
# def create_test_data():
#     with open("src/Mocked.json", "r", encoding = "UTF-8") as file:
#         data = json.load(file)

#     places = [Place(p) for p in data]

#     return places


if __name__ == "__main__":
    places = Place.get_places("کافه 90")