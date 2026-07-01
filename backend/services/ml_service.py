import os
try:
    import joblib
    import pandas as pd
    import numpy as np
    ML_LIBS_AVAILABLE = True
except ImportError:
    ML_LIBS_AVAILABLE = False

class MLService:
    def __init__(self):
        self.tf_model = None
        self.preprocessor = None
        self.kmeans = None
        self.rf_clf = None
        
        self.models_dir = os.path.join(os.path.dirname(__file__), '../../models')
        self._load_models()

    def _load_models(self):
        try:
            # We try to load standard ML models if they exist
            if os.path.exists(os.path.join(self.models_dir, 'preprocessor.pkl')):
                self.preprocessor = joblib.load(os.path.join(self.models_dir, 'preprocessor.pkl'))
            if os.path.exists(os.path.join(self.models_dir, 'kmeans_model.pkl')):
                self.kmeans = joblib.load(os.path.join(self.models_dir, 'kmeans_model.pkl'))
            if os.path.exists(os.path.join(self.models_dir, 'rf_classifier.pkl')):
                self.rf_clf = joblib.load(os.path.join(self.models_dir, 'rf_classifier.pkl'))
                
            # For TF, we import locally to avoid overhead if not used
            if os.path.exists(os.path.join(self.models_dir, 'startup_success_model.h5')):
                import tensorflow as tf
                self.tf_model = tf.keras.models.load_model(os.path.join(self.models_dir, 'startup_success_model.h5'))
                print("Loaded TF Model")
        except Exception as e:
            print(f"Warning: Could not load all ML models: {e}")

    def predict_success(self, startup_data):
        if ML_LIBS_AVAILABLE and self.tf_model and self.preprocessor:
            try:
                df = pd.DataFrame([startup_data])
                processed = self.preprocessor.transform(df)
                pred = self.tf_model.predict(processed)[0][0]
                return {"success_probability": round(float(pred) * 100, 2), "method": "TensorFlow DNN"}
            except Exception as e:
                print(f"TF Prediction failed: {e}")
        
        # Fallback Heuristic if models aren't loaded (e.g. Python 3.14 issue)
        return self._heuristic_prediction(startup_data)
        
    def _heuristic_prediction(self, data):
        score = 50
        # Simple heuristic mimicking the data generation logic
        if data.get('Industry') in ['AI', 'Cybersecurity', 'Fintech']: score += 15
        if 5 <= data.get('Team_Size', 0) <= 20: score += 10
        if data.get('Innovation_Score', 0) > 7: score += 15
        if data.get('Competition_Level') == 'Low': score += 10
        elif data.get('Competition_Level') == 'High': score -= 10
        
        score = min(max(score, 10), 98) # Clamp between 10 and 98
        return {"success_probability": score, "method": "Heuristic Engine (Fallback)"}

    def get_cluster(self, startup_data):
        if ML_LIBS_AVAILABLE and self.kmeans and self.preprocessor:
            try:
                df = pd.DataFrame([startup_data])
                processed = self.preprocessor.transform(df)
                cluster = self.kmeans.predict(processed)[0]
                return int(cluster)
            except:
                pass
        import random
        return random.randint(0, 5)

ml_service = MLService()
