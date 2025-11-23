# backend/tests/test_analyze.py
import requests

URL = "http://localhost:8000/analyze"

with open("test_plant.jpg", "rb") as img:
    files = {"image": ("test.jpg", img, "image/jpeg")}
    res = requests.post(URL, files=files)

print(res.status_code)
print(res.json())