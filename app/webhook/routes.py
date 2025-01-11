from flask import Blueprint, jsonify, request, render_template
from datetime import datetime, timedelta
from app.logcontrol import logger
from app.extensions import logs_db

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook.route('/')
def welcome():
    logger('webhook').info("Welcome endpoint accessed")
    return jsonify(message="Welcome", status=200), 200

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers.get('Content-Type') == "application/json":
        payload = request.json
        try:
            action = payload.get('action', "unknown")
            author = "No data"
            from_branch = "No data"
            to_branch = "No data"
            request_id = "No data"

            if action in ['opened', 'closed', 'synchronize']:
                pr_data = payload.get('pull_request', {})
                request_id = pr_data.get('id', "No data")
                author = pr_data.get('user', {}).get('login', "No data")
                from_branch = pr_data.get('head', {}).get('ref', "No data")
                to_branch = pr_data.get('base', {}).get('ref', "No data")

                if action == "closed":
                    action = "merged" if pr_data.get("merged", False) else "closed without merge"


            elif "head_commit" in payload and "pusher" in payload:
                request_id = payload.get('head_commit', {}).get('id', "No data")
                author = payload.get('pusher', {}).get('name', "No data")
                action = "pushed"
                to_branch = payload.get('ref', "None").split('/')[-1]
                from_branch = payload.get('base_ref', "None")

            logger('webhook/receiver').info(f"Action processed: {action}")

        except Exception as e:
            logger('webhook/receiver').error(f"Error processing data: {e}")
            return jsonify(message=f"Invalid data: {e}", status=400), 400

        timestamp = datetime.utcnow()


        document = {
            "request_id": request_id,
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        try:
            logs_db.insert_one(document)
            logger('Database').info("Document successfully stored in MongoDB")
            return jsonify(message="Data stored successfully", status=200), 200
        except Exception as e:
            logger('Database').error(f"Failed to store document: {e}")
            return jsonify(message=f"Database error: {e}", status=500), 500

    logger('webhook/receiver').warning("Unsupported content type")
    return jsonify(message="Unsupported content type", status=415), 415

@webhook.route('/ui', methods=["GET"])
def ui():
    return render_template("index.html", Title="Recent Repo Events")

@webhook.route('/ui/data', methods=["GET"])
def ui_data():
    def format_suffix(day):
        if 11 <= day <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    recent_tasks = []
    time_threshold = datetime.utcnow() - timedelta(seconds=15)

    for record in logs_db.find({'timestamp': {'$gte': time_threshold}}):
        record.update({
            "author": str(record.get('author', '')),
            "request_id": str(record.get('request_id', '')),
            "from_branch": str(record.get('from_branch', '')),
            "to_branch": str(record.get('to_branch', '').split('/')[-1]),
            "action": str(record.get('action', '')),
            "timestamp": record['timestamp'].strftime(f"%d{format_suffix(record['timestamp'].day)} %B %Y - %I:%M %p UTC"),
            "_id": str(record.get('_id', ''))
        })
        recent_tasks.append(record)

    logger("ui/data").info("Data retrieved successfully from MongoDB")
    return jsonify(recent_tasks), 200
