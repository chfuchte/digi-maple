import requests
import os, sys
import time
import cv2
import numpy as np

logged_in = False

session = requests.Session()

while not logged_in:

    os.system("clear")

    method: int = int(input("1: Login\n2: Register\n3: Guest\n> "))

    full_name: str = ""
    email: str = ""
    password: str = ""

    if method == 1:
        url = 'http://127.0.0.1:8080/api/auth/login'
        os.system("clear")

        if not email and not password:
            email = input("email: ")
            password = input("password: ")

        login_request: dict[str] = {"email": email, "password": password}

        json_message = session.post(url, json = login_request).json()
        try:
            if json_message["message"] == "Logged in":
                logged_in = True
                print("User logged in!")
                time.sleep(2)
            else:
                logged_in = False
                print("Failed to login")
                time.sleep(2)
        except KeyError:
            logged_in = False
            try:
                print(json_message["error"])
                time.sleep(2)
            except KeyError:
                print(json_message["detail"][0]["msg"])
                time.sleep(2)


    elif method == 2:
        url = 'http://127.0.0.1:8080/api/auth/register'
        os.system("clear")
        full_name = input("name: ")
        email = input("email: ")
        password = input("password: ")

        register_request: dict[str] = {"full_name": full_name, "email": email, "password": password}

        json_message = session.post(url, json = register_request).json()

        try:
            if json_message["message"] == "User created":
                print("User created")
            else:
                print("Failed to create user")
        except KeyError:
            print(json_message["error"])
            time.sleep(2)
            continue


        login_request: dict[str] = {"email": email, "password": password}

        url = 'http://127.0.0.1:8080/api/auth/login'
        json_message = session.post(url, json = login_request).json()
        try:
            if json_message["message"] == "Logged in":
                logged_in = True
            else:
                logged_in = False
        except KeyError:
            print(json_message["error"])
            time.sleep(2)
            continue


    elif method == 3:
        break


os.system("clear")

running = True

if logged_in:
    url = 'http://127.0.0.1:8080/api/auth/whoami'
    current_uid = session.get(url).json()["id"]
else:
    current_uid = None



while running:

    os.system("clear")

    if logged_in:
        print("\t\t\tLogged in:")
    else:
        print("\t\t\tLogged out")

    selection = int(input("Main interface\n\n1: Upload map\n2: Search maps"))

    if selection == 1:
        if not logged_in:
            print("User not logged in. This feature is only available for logged in users")
            time.sleep(2)
            os.system("clear")
            continue

        # Set the name

        map_name: str = input("Map name: ")

        url = 'http://127.0.0.1:8080/api/maps'
        create_map_request: dict[str, str] = {"name": map_name, "user_id": int(current_uid)}

        json_message = session.post(url, json = create_map_request).json()

        map_id = json_message["id"]


        # Upload image

        image_path: str = input("Image file path: ")

        url = 'http://127.0.0.1:8080/api/maps/upload/' + str(map_id)
        upload_image_request: dict[str, str] = {"name": map_name, "user_id": int(current_uid)}


        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)

        print(response.status_code)
        print(response.json())


    elif selection == 2:
        map_name: str = input("Map name: ")

        url = 'http://127.0.0.1:8080/api/maps/search/' + map_name

        json_message = session.get(url).json()[0]
        print(json_message)

        img_url = json_message["imgUrl"]
        resp = requests.get(img_url)

        if resp.status_code == 200:
            image_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if image is not None:
                cv2.imshow("Map", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("❌ Failed to decode image")
        else:
            print(f"❌ Failed to download image: HTTP {resp.status_code}")

        input("Press Enter to continue...")  # Prevents loop from racing forward





