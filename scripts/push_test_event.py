import requests

try:
    response = requests.post("https://pitchload.net/api/v1/events/",
        json={},
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {""}"
        },
    )

    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")