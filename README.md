# Webhook Receiver

This project is a Flask-based web application designed to track and store actions performed on a GitHub repository in a MongoDB database. The application leverages GitHub's webhook functionality to capture events such as pushes, pull requests, and merges in real time. These events are then stored in the database for persistence and further analysis.

The application includes a real-time user interface (UI) that automatically refreshes every 15 seconds to display the latest actions in a clear and concise format. 

For example:

When a user pushes a commit, the interface shows details such as the author, the branch to which the commit was pushed, and the timestamp of the action.

For pull requests, it displays the author, the source and target branches, and the timestamp of the pull request creation or update.

When a branch is merged, the UI highlights the author, source branch, target branch, and merge timestamp.

*******************

## Setup

* Create a new virtual environment

```bash
python -m venv .venv
```

* Activate the virtual env

```bash
.\.venv\Scripts\Activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application

```bash
python run.py
```
* Create a `.env` file which contains:
```bash

MONGO_URI=
host =
port =
```
  
* Access the frontend through:
  
`frontend/index.html`

*******************
