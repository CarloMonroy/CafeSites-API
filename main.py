from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")
## HTTP GET - Read Record
@app.route("/random")
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def all():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route("/search")
def search():
    query_location = request.args.get('loc')
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    return jsonify(error={"Error": "Sorry, we don't have a cafe at that location."})

## HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_coffe():
    new_coffe = Cafe(
    name = request.form.get('name'),
    map_url = request.form.get('map_url'),
    img_url = request.form.get('img_url'),
    location = request.form.get('location'),
    seats = request.form.get('seats'),
    has_toilet = bool(request.form.get('has_toilet')),
    has_wifi = bool(request.form.get('has_wifi')),
    has_sockets = bool(request.form.get('has_sockets')),
    can_take_calls = bool(request.form.get('can_take_calls')),
    coffee_price = request.form.get('coffee_price'),
    )
    db.session.add(new_coffe)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record

@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    return jsonify(error={"Error": "Sorry, we don't have a cafe at that location."})

## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete(cafe_id):
    if request.args.get('api_key') == 'TopSecretAPIKey':
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe."})
        return jsonify(error={"Error": "There was not fount any cafe with that id in database"})
    return jsonify(error={"Error": "Not allowed, make sure you have the correct api key."})

if __name__ == '__main__':
    app.run(debug=True)
