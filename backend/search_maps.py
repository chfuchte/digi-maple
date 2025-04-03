from difflib import SequenceMatcher
import requests

def search(query: str, maps: dict) -> list:
    name_list = []

    for _, value in maps.items():
        name_list.append((value["name"], value["id"]))

    def similar(name):
        return SequenceMatcher(None, name[0], query).ratio()

    return sorted(name_list, key=similar, reverse=True)


if __name__ == "__main__":
    map_list = requests.get("http://127.0.0.1:8080/maps").json()["value"]

    print(search("bockenheim", map_list))
