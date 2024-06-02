from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

description_templates = [
    "Hi, I'm {first_name}, a {age}-year-old from {city}, {country}. I love spending time outdoors and exploring new places.",
    "Hello, I'm {first_name}, {age} years old, living in {city}, {country}. In my free time, I enjoy reading books and cooking new recipes.",
    "Hey there! I'm {first_name}, a {age}-year-old from {city}, {country}. I'm passionate about technology and love learning new programming languages."
]

# Liste pour stocker les matches
matches = []

@app.route('/profiles', methods=['GET'])
def get_profiles():
    n = request.args.get('n', default=10, type=int)
    response = requests.get(f'https://randomuser.me/api/?results={n}')
    data = response.json()
    
    profiles = []
    for profile in data['results']:
        first_name = profile['name']['first']
        age = profile['dob']['age']
        city = profile['location']['city']
        country = profile['location']['country']
        
        description = random.choice(description_templates)
        description = description.format(first_name=first_name, age=age, city=city, country=country)
        
        profile['description'] = description
        profiles.append(profile)
    
    return jsonify(profiles)

@app.route('/match', methods=['POST'])
def match_profile():
    data = request.json
    user_id = data.get('user_id')
    liked = data.get('liked')
    
    # Ajouter le match à la liste des matches
    matches.append({'user_id': user_id, 'liked': liked})
    
    return jsonify({'user_id': user_id, 'liked': liked, 'status': 'success'}), 200

@app.route('/matches', methods=['GET'])
def get_matches():
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
