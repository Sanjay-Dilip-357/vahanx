from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_vehicle_details(registration_number):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    url = f"https://vahanx.in/rc-search/{registration_number}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}

    all_ele = soup.find_all('div', class_=['col-sm-6', 'col-12'])
    for ele in all_ele:
        span = ele.find('span')
        p = ele.find('p')
        if span and p:
            label = span.get_text(strip=True)
            value = p.get_text(strip=True)
            data[label] = value

    card_sections = soup.find_all('div', class_='hrcd-cardbody')
    for card in card_sections:
        span = card.find('span')
        p = card.find('p')
        if span and p:
            label = span.get_text(strip=True)
            value = p.get_text(strip=True)
            if label not in data:
                data[label] = value

    return data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    reg_no = request.json.get("registration_number", "").upper()

    if not reg_no:
        return jsonify({"error": "Invalid registration number"}), 400

    data = get_vehicle_details(reg_no)

    if not data:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
