#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Hero, Power, hero_powers, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return """<h1>Superheroes</h1>"""


@app.route("/heroes")
def get_heroes():
    heroes = Hero.query.all()

    hero_dict = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]

    response = make_response(jsonify(hero_dict), 200)

    return response


@app.route("/heroes/<int:hero_id>", methods=["GET"])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)

    if request.method == "GET":
        if not hero:
            response_body = {"error": "Hero not found"}
            response = make_response(jsonify(response_body), 404)
            return response

        powers_dict = [
            {"id": power.id, "name": power.name, "description": power.description}
            for power in hero.powers
        ]

        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": powers_dict,
        }

        response = make_response(jsonify(hero_dict), 200)

        return response


@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()

    powers_dict = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]

    response = make_response(jsonify(powers_dict), 200)

    return response


@app.route("/powers/<int:power_id>", methods=["GET"])
def get_powers_by_id(power_id):
    power = Power.query.get(power_id)
    if request.method == "GET":
        if not power:
            response_body = {"error": "Power not found"}
            response = make_response(jsonify(response_body), 404)
            return response

        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }

        response = make_response(jsonify(power_data), 200)

        return response


@app.route("/powers/<int:power_id>", methods=["PATCH"])
def update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)

    data = request.get_json()
    if "description" not in data:
        return make_response(jsonify({"error": "Description is required"}), 400)

    description = data["description"]
    power.description = description

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)

    power_data = {"id": power.id, "name": power.name, "description": power.description}

    response = make_response(jsonify(power_data), 200)

    return response

@app.route('/hero_power', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not power_id or not hero_id:
        return make_response(jsonify({'errors': ['Validation errors']}), 400)

    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if not power or not hero:
        return make_response(jsonify({'error': 'Power or Hero not found'}), 404)

    hero_power_instance = HeroPower(power=power, hero=hero)
    db.session.add(hero_power_instance)
    db.session.commit()

    powers = [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    response = make_response(jsonify(hero_data), 200)

    return response


if __name__ == "__main__":
    app.run(port=5565, debug=True)
