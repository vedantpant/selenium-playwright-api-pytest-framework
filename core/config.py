import os

class Config:

    BASE_URL = os.getenv("BASE_URL","https://www.saucedemo.com")
    BROWSER = os.getenv("BROWSER","chrome")
    HEADLESS = os.getenv("HEADLESS","false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT",10))
