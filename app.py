import time
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Твои ключи (совет: не делись ими в публичном доступе)
CLIENT_ID = "3w729rzyygngddusvrnayve46uhp9t"
CLIENT_SECRET = "9h2x87by844s8d7zsc3lbldas05oho"

# Список логинов стримеров
STREAMERS = ["moneymate_", "Ivanmiks", "maryapozs", "kripero4ek2014"]

# Кэш для токена, чтобы Twitch не забанил за частые запросы
token_cache = {
    "access_token": None,
    "expires_at": 0
}

def get_access_token():
    if token_cache["access_token"] and time.time() < token_cache["expires_at"] - 60:
        return token_cache["access_token"]

    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, params=params)
    data = response.json()
    
    token_cache["access_token"] = data["access_token"]
    token_cache["expires_at"] = time.time() + data["expires_in"]
    
    return data["access_token"]

def get_live_streams():
    try:
        token = get_access_token()
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}"
        }
        url = "https://api.twitch.tv/helix/streams"
        params = [("user_login", s) for s in STREAMERS]

        response = requests.get(url, headers=headers, params=params)
        return response.json().get("data", [])
    except Exception as e:
        print(f"Ошибка получения стримов: {e}")
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/streams")
def streams():
    return jsonify(get_live_streams())

if __name__ == "__main__":
    app.run(debug=True)