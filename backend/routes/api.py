from flask import Blueprint, request, jsonify
from services.gemini_service import GeminiService
from services.ml_service import ml_service
from cv.pitch_deck_analyzer import PitchDeckAnalyzer
from database.mongo import db
import os

api_bp = Blueprint('api', __name__)
gemini = GeminiService()
cv_analyzer = PitchDeckAnalyzer()

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "db_connected": db.is_connected()})

@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    user = db.create_user(data.get('email'), data.get('password'), data.get('name'))
    if user:
        return jsonify({"message": "User created successfully", "user": user}), 201
    return jsonify({"error": "User already exists"}), 400

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = db.authenticate_user(data.get('email'), data.get('password'))
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@api_bp.route('/analyze/startup', methods=['POST'])
def analyze_startup():
    data = request.json
    # Expected: Industry, Team_Size, Market_Size_B, Revenue_Model, Competition_Level, Innovation_Score
    user_id = data.pop('user_id', 'mock_user')
    startup_details = data.get('details', str(data))
    
    # 1. ML Prediction
    prediction = ml_service.predict_success(data)
    
    # 2. Gemini GenAI Features
    insights = gemini.generate_all_insights(startup_details)
    
    analysis_result = {
        "input_data": data,
        "prediction": prediction,
        "swot": insights.get('swot', ''),
        "roadmap": insights.get('roadmap', ''),
        "bmc": insights.get('bmc', ''),
        "competitors": insights.get('competitors', ''),
        "funding": insights.get('funding', ''),
        "pitch": insights.get('pitch', '')
    }
    
    # Save to DB
    doc_id = db.save_analysis('startup_analyses', user_id, analysis_result)
    analysis_result['_id'] = doc_id
    
    return jsonify(analysis_result), 200

@api_bp.route('/analyze/pitchdeck', methods=['POST'])
def analyze_pitchdeck():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    user_id = request.form.get('user_id', 'mock_user')
    
    # Save file temporarily
    temp_path = os.path.join('/tmp', file.filename)
    file.save(temp_path)
    
    try:
        # Run CV Analysis
        cv_results = cv_analyzer.analyze_pdf(temp_path)
        
        # Save to DB
        cv_results['filename'] = file.filename
        doc_id = db.save_analysis('pitch_deck_reports', user_id, cv_results)
        cv_results['_id'] = doc_id
        
        return jsonify(cv_results), 200
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    history = data.get('history', [])
    context = data.get('context', '')
    
    reply = gemini.chat(message, history, context)
    return jsonify({"reply": reply}), 200

@api_bp.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    startups = db.get_analyses('startup_analyses', user_id)
    pitch_decks = db.get_analyses('pitch_deck_reports', user_id)
    return jsonify({"startups": startups, "pitch_decks": pitch_decks}), 200
