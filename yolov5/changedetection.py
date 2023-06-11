import os
import cv2
import pathlib
import requests
from datetime import datetime


class TokenNotReceived(Exception):
    pass


class ChangeDetection:
    previous_results = []
    HOST = 'http://127.0.0.1:8000'
    username = 'admin'
    password = 'admin123!@#'
    token = ''
    title = ''
    text = ''
    session = requests.Session()

    def __init__(self, names):
        self.previous_results = [0 for _ in range(len(names))]

        response = self.session.post(
            f"{self.HOST}/api-token-auth/",
            data={
                "username": self.username,
                "password": self.password,
            },
        )

        response.raise_for_status()
        self.token = response.json().get("token", "")

        if not isinstance(self.token, str) or len(self.token) == 0:
            raise TokenNotReceived
        else:
            print("[SUCCESS] token :", self.token)

    def add(self, names, currently_detected, save_dir, image):
        self.title = ""
        self.text = ""

        is_changed = False
        i = 0
        while i < len(self.previous_results):
            if self.previous_results[i] is False and currently_detected[i] is True:
                is_changed = True

                self.title = f"{names[i]} detected"
                self.text += names[i] + ", "

            i += 1

        self.previous_results = currently_detected[:]

        if is_changed:
            self.send(save_dir, image)

    def send(self, save_dir, image):
        now = datetime.utcnow()

        save_dir = os.getcwd() / save_dir / 'detected' / str(now.year) / str(now.month) / str(now.day)
        pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

        filename = f"{now.hour}-{now.minute}-{now.second}-{now.microsecond}.jpg"
        filepath = save_dir / filename

        resized_image = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(filepath, resized_image)

        headers = {
            "Authorization": f"Token {self.token}",
            "Accept": "application/json",
        }

        data = {
            "title": self.title,
            "text": self.text,
            "created_date": now,
            "published_date": now,
        }

        files = {"image": open(filepath, "rb")}
        response = self.session.post(
            f"{self.HOST}/api_root/Post/",
            headers=headers, data=data, files=files,
        )

        if response.status_code == 200:
            print("[SUCCESS] response.status_code :", response.status_code)

        print("[DEBUG] response.text :", response.text)
