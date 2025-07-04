from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

def insert_event(data, event_type):
    author = data['pusher']['name'] if event_type == 'push' else data['sender']['login']
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    if event_type == 'push':
        event = {
            'message': f'{author} pushed to {data["ref"].split("/")[-1]} on {timestamp}'
        }
    elif event_type == 'pull_request':
        pr = data['pull_request']
        event = {
            'message': f'{author} submitted a pull request from {pr["head"]["ref"]} to {pr["base"]["ref"]} on {timestamp}'
        }
    else:
        return  # ignore other events

    collection.insert_one(event)

def get_latest_events():
    return list(collection.find().sort('_id', -1).limit(10))
