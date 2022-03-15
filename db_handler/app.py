from flask import Flask, request
from yaml import safe_load
from pymongo import MongoClient

# config = safe_load(open('./db_handler/db_config.yaml', 'r'))
config = safe_load(open('db_config.yaml', 'r'))
DB_HOST = config['host']
DB_PORT = config['port']
DB_USERNAME = config['username']
DB_PASSWORD = config['password']
app = Flask(__name__)
client = MongoClient(f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}")
db = client.iaml_automation
collection = db.eventlist


@app.route('/add', methods=['POST'])
def add_document():
    if request.method == 'POST':
        try:
            result = collection.insert_one(request.json)
            return "Request Succeeded"
        except Exception as e:
            print("An exception occurred ::", e)
            return str(e), 500


@app.route('/add_many', methods=['POST'])
def add_documents():
    if request.method == 'POST':
        try:
            events = request.json["events"]
        except KeyError as e:
            print("An exception occurred ::", e)
            return "the given request body does not contain key `events`", 500
        try:
            result = collection.insert_many(events)
            print(result.inserted_ids)
            return "Request Succeeded"
        except Exception as e:
            print("An exception occurred ::", e)
            return str(e), 500


if __name__ == "__main__":
    app.run()  # from waitress import serve  #  # serve(app, host="0.0.0.0", port=5000)
