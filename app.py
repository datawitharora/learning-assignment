from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi
import json
import os
load_dotenv()
app = Flask(__name__)

#mongodb connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority")


# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
db = client["assignment_db"]
collection = db["users"]

@app.route('/api', methods=['GET'])
def get_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #1. extract data from html form

        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        document = {
            "name" : name,
            "email" : email,
            "role" : role
        }

        #2. try insert data into mongodb
        try:
            collection = db["users"]
            collection.insert_one(document)
            return redirect(url_for('success'))
        except Exception as e:
            return render_template('index.html', error=str(e)), 

    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')



if __name__ == '__main__':
    app.run(debug=True)

