## 1️⃣ **app/__init__.py**

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import routes

## 2️⃣ **app/models.py**

from app import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

## 3️⃣ **app/routes.py**

from flask import request, jsonify
from app import app, db
from app.models import Vehicle

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.json
    new_vehicle = Vehicle(make=data['make'], model=data['model'], year=data['year'])
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle added successfully!'}), 201

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{'id': v.id, 'make': v.make, 'model': v.model, 'year': v.year} for v in vehicles])

@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    data = request.json
    vehicle.make = data.get('make', vehicle.make)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    db.session.commit()
    return jsonify({'message': 'Vehicle updated successfully'})

@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'})
