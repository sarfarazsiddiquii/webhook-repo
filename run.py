from app import create_app
from app.logcontrol import logger
import os
from dotenv import load_dotenv

app = create_app()
load_dotenv()
host = os.getenv('HOST', '127.0.0.1')
port = os.getenv('PORT', '5000')

if __name__ == '__main__': 
    logger("app").info("App running...")
    from waitress import serve
    serve(app, host=host, port=int(port))
    
    