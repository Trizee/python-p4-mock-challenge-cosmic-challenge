#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''

class Scientists(Resource):
    
    def get(self):
        scientists = [sci.to_dict(rules=('-missions',)) for sci in Scientist.query.all()]
        return make_response(
            jsonify(scientists),
            200
        )
    
    def post(self):

        data = request.get_json()

        try:
            new_scientist = Scientist(
                name = data.get('name'),
                field_of_study = data.get('field_of_study')
            )
        except ValueError:
            return make_response(jsonify({"errors": ["validation errors"]}),400)
        
        db.session.add(new_scientist)
        db.session.commit()

        return make_response(
            jsonify(new_scientist.to_dict()),
            201
        )
    
api.add_resource(Scientists,'/scientists')
    
class ScientistById(Resource):

    def get(self,id):

        scientist = Scientist.query.filter_by(id = id).first()

        if not scientist:
            return make_response(
                jsonify({"error": "Scientist not found"}),
                404
            )

        return make_response(
            jsonify(scientist.to_dict()),
            200
        )

    def patch(self,id):

        data = request.get_json()

        scientist = Scientist.query.filter_by(id = id).first()

        if not scientist:
            return make_response(
                jsonify({"error": "Scientist not found"}),
                404
            )
        
        try:
            for field in data:
                setattr(scientist,field,data[field])

            db.session.add(scientist)
            db.session.commit()

            return make_response(
                jsonify(scientist.to_dict(rules=('-missions',))),
                202
            )
        except ValueError:
            return make_response(
                jsonify({"errors": ["validation errors"]}),
                400

            )
        
    def delete(self,id):

        scientist = Scientist.query.filter_by(id = id).first()

        if not scientist:
            return make_response(
                jsonify({"error": "Scientist not found"}),
                404
            )
        
        db.session.delete(scientist)
        db.session.commit()

        return make_response(
            jsonify({}),
            204
        )
    
api.add_resource(ScientistById,'/scientists/<int:id>')

class Planets(Resource):

    def get(self):
        planets = [planet.to_dict(rules=('-missions',)) for planet in Planet.query.all()]
        return make_response(jsonify(planets),200)

api.add_resource(Planets,'/planets')

class Missions(Resource):

    def post(self):
        data = request.get_json()

        try:
            new_missions = Mission(
                name = data.get('name'),
                scientist_id = data.get('scientist_id'),
                planet_id = data.get('planet_id')
            )
        except ValueError:
            return make_response(
                jsonify({"errors": ["validation errors"]}),
                400
            )
        
        db.session.add(new_missions)
        db.session.commit()

        return make_response(
            jsonify(new_missions.to_dict()),
            201
        )

api.add_resource(Missions,'/missions')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
