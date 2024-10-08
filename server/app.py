# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # Query the database for the earthquake with the specified ID
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        # If found, return the attributes as a JSON response
        response = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return jsonify(response), 200
    else:
        # If not found, return an error message
        response = {
            "message": f"Earthquake {id} not found."
        }
        return jsonify(response), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods = ['GET'])
def get_minimum_magnitude(magnitude):

    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the response data
    quake_list = [{
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    } for quake in quakes]
    
    response = {
        "count": len(quake_list),
        "quakes": quake_list
    }
    
    return jsonify(response), 200
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)
