from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def create_app():
    app = Flask(__name__)
    CORS(app) # Allow cross-origin requests from Streamlit
    
    # Connect to MongoDB
    from database.mongo import db
    db.connect()
    
    # Register Blueprints
    from routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return "VenturePilot API is running."
        
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
