import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib
import os

def train_and_save_sklearn_models():
    print("Loading data for Scikit-Learn models...")
    df = pd.read_csv('../../data/startups.csv')
    
    # We will use the preprocessed data from TF pipeline if possible, 
    # but for simplicity, we'll re-load the preprocessor
    preprocessor = joblib.load('../../models/preprocessor.pkl')
    
    X = df.drop(['Success_Probability', 'Success_Class'], axis=1)
    y_prob = df['Success_Probability']
    y_class = df['Success_Class']
    
    X_processed = preprocessor.transform(X)
    
    # 1. KMeans Clustering (Startup Clustering)
    print("Training KMeans...")
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X_processed)
    joblib.dump(kmeans, '../../models/kmeans_model.pkl')
    
    # 2. NearestNeighbors (Startup Similarity Detection)
    print("Training NearestNeighbors...")
    nn_model = NearestNeighbors(n_neighbors=5, algorithm='auto')
    nn_model.fit(X_processed)
    joblib.dump(nn_model, '../../models/nn_model.pkl')
    
    # 3. Random Forest Classifier (Viability Analysis & Feature Importance)
    print("Training Random Forest Classifier...")
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(X_processed, y_class)
    joblib.dump(rf_clf, '../../models/rf_classifier.pkl')
    
    # Extract and save feature names for importance
    # Get feature names from ColumnTransformer
    num_features = preprocessor.named_transformers_['num'].get_feature_names_out()
    cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out()
    all_features = list(num_features) + list(cat_features)
    
    # Save feature names alongside feature importance
    importance_df = pd.DataFrame({
        'Feature': all_features,
        'Importance': rf_clf.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    importance_df.to_csv('../../models/feature_importance.csv', index=False)
    
    # Also save the base DataFrame to find similar startups by index later
    df.to_csv('../../models/startup_database.csv', index=False)
    
    print("Saved Scikit-Learn models and feature importances to models/")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_and_save_sklearn_models()
