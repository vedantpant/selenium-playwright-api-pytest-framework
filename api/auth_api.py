import requests


class AuthAPI:

    BASE_URL = "https://dummyjson.com"

    def login(self, username, password):

        url = f"{self.BASE_URL}/auth/login"

        payload = {
            "username": username,
            "password": password
        }

        response = requests.post(url, json=payload)
        return response

