from flask_marshmallow import Marshmallow
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import jsonify, request

from db_utils.filter_utils.date_filter import get_filter_by_args

from sqlalchemy.sql import func

from db_utils.db_uri import mariadb_uri_2

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = mariadb_uri_2()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class Saludos(db.Model):
    __tablename__ = "saludos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date(),
                           server_default=func.now())

class SaludosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Saludos
        load_instance = True
        sqla_session = db.session

saludo_schema = SaludosSchema()
saludos_schema = SaludosSchema(many=True)

@app.route("/")
def index():
    return jsonify({"Message": "Correcto"})

@app.route('/saludos', methods=['GET'])
def retrieve():
    args = request.args.to_dict()
    if args:
        filter = get_filter_by_args(args, Saludos)
        saludos = Saludos.query.filter(*filter)
    else:
        saludos = Saludos.query.all()
    return saludos_schema.dump(obj=saludos)

@app.route('/saludos', methods=['POST'])
def create():
    data = request.json
    new_hi = saludo_schema.load(data, session=db.session)
    db.session.add(new_hi)
    db.session.commit()
    return saludo_schema.dump(new_hi), 201

@app.route('/saludos/<pk>', methods=['PUT', 'PATCH'])
def update(pk):
    data = request.json
    existing_Saludos = Saludos.query.filter(Saludos.id == pk).one_or_none()
    if existing_Saludos:
        update_Saludos = saludo_schema.load(data=data, session=db.session)
        existing_Saludos.message = update_Saludos.message
        db.session.merge(existing_Saludos)
        db.session.commit()
        return saludo_schema.dump(existing_Saludos), 201
    else:
        return jsonify({
            "Error": "Not found"
        })

@app.route('/saludos/<pk>', methods=['DELETE'])
def delete(pk):
    obj = Saludos.query.filter(Saludos.id == pk).one_or_none()
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": f"successfully deleted"})
    else:
        return jsonify({"message": f"Not found"})


@app.route('/saludo/<pk>', methods=['GET'])
def get_one(pk):
    obj = Saludos.query.filter(Saludos.id == pk).one_or_none()

    if obj is not None:
        return saludo_schema.dump(obj)
    else:
        return jsonify({"message": f"Not found"})
