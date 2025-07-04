
from flask import Flask, request, render_template, jsonify
from db import db, insert_event, get_latest_events
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    events = get_latest_events()
    return render_template('index.html', events=events)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    insert_event(data, event_type)
    return '', 204

@app.route('/poll')
def poll():
    events = get_latest_events()
    return jsonify(events)

if __name__ == '__main__':
    db.connect()
    app.run(debug=True)
