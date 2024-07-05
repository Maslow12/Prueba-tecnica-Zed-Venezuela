from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models.greetings.saludos import Saludos
from schemas.greetings.saludos import SaludosSchema
from app import app

app_saludos = Blueprint('app_saludos', __name__)

db = SQLAlchemy(app)

@app_benefits.route('/saludos', methods=['GET'])
def retrieve():
    people = Saludos.query.all()
    return SaludosSchema.dump(people)


@app_benefits.route('/saludos', methods=['POST'])
def create():
    data = request.data
    new_hi = SaludosSchema.load(data, session=db.session)
    db.session.add(new_hi)
    db.session.commit()
    return SaludosSchema.dump(new_hi), 201


@app_benefits.route('/saludos/<pk>', methods=['PUT', 'PATCH'])
def update(pk):
    existing_Saludos = Saludos.query.filter(Saludos.id == pk).one_or_none()

    if existing_Saludos:
        update_Saludos = SaludosSchema.load(Saludos, session=db.session)
        existing_Saludos.fname = update_Saludos.fname
        db.session.merge(existing_Saludos)
        db.session.commit()
        return SaludosSchema.dump(existing_Saludos), 201
    else:
        return jsonify({
            "Error": "Not found"
        })


@app_benefits.route('/saludos/<pk>', methods=['DELETE'])
def delete(pk):
    obj = Saludos.query.filter(Saludos.id == pk).one_or_none()

    if obj:
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message":f"successfully deleted"})
    else:
        return jsonify({"message": f"Not found"})


@app_benefits.route('/saludos/get_one/<pk>', methods=['GET'])
def get_one(pk):
    obj = Saludos.query.filter(Saludos.id == pk).one_or_none()

    if Saludos is not None:
        return SaludosSchema.dump(obj)
    else:
        return jsonify({"message": f"Not found"})
