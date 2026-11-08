from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder="static")

ESPN = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/scoreboard")
def scoreboard():
    date = request.args.get("date", "")

    if date and (len(date) != 8 or not date.isdigit()):
        return jsonify({"error": "Data inválida"}), 400

    return proxy(
        f"{ESPN}/scoreboard",
        {"dates": date} if date else {}
    )

@app.route("/api/player-gamelog/<int:athlete_id>")
def player_gamelog(athlete_id):
    season = request.args.get("season", "2026")

    url = (
        "https://site.api.espn.com/apis/common/v3/"
        f"sports/basketball/nba/athletes/{athlete_id}/gamelog"
    )

    return proxy(url, {"season": season})

def proxy(url, params):
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return jsonify(response.json())

    except requests.RequestException as exc:
        return jsonify({
            "error": "Fonte ESPN indisponível",
            "detail": str(exc)
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
