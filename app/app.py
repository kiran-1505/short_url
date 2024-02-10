from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Create a database model for URLs
class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(4))

def create_shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=4)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

def get_or_create_short_url(long_url):
    found_url = Urls.query.filter_by(long=long_url).first()
    if found_url:
        return found_url.short
    else:
        short_url = create_shorten_url()
        new_url = Urls(long=long_url, short=short_url)
        db.session.add(new_url)
        db.session.commit()
        return short_url

@app.route("/shorten", methods=["POST"])
def shorten_url():
    """
    Let's a developer create a short url from a long one
    and if it already exists then just return
    
    Input and output will be in JSON format
    """
    data = request.json
    long_url = data.get('long_url')
    if long_url:
        short_url = get_or_create_short_url(long_url)
        response = {"long_url": long_url, "short_url": short_url}
        return jsonify(response), 200
    else:
        return jsonify({"error": "Missing long_url parameter"}), 400

@app.route("/long_url", methods=["GET"])
def get_long_url():
    """
    Let's a developer get the long url from a short one
    Input and output will be in JSON format.
    """
    short_url = request.args.get('short_url')
    if short_url:
        found_url = Urls.query.filter_by(short=short_url).first()
        if found_url:
            return jsonify({"short_url": short_url, "long_url": found_url.long}), 200
        else:
            return jsonify({"error": "Short URL not found"}), 404
    else:
        return jsonify({"error": "Missing short_url parameter"}), 400

@app.route("/delete_url", methods=["DELETE"])
def delete_url():
    """
    Let's a developer delete a url from the database
    Input and output will be in JSON format
    """
    data = request.json
    short_url = data.get('short_url')
    if short_url:
        url_to_delete = Urls.query.filter_by(short=short_url).first()
        if url_to_delete:
            db.session.delete(url_to_delete)
            db.session.commit()
            return jsonify({"message": f"Short URL {short_url} deleted successfully"}), 200
        else:
            return jsonify({"error": "Short URL not found"}), 404
    else:
        return jsonify({"error": "Missing short_url parameter"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
