import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
import os

def train_and_save_tf_model():
    print("Loading data...")
    df = pd.read_csv('../../data/startups.csv')
    
    # Features and Target
    X = df.drop(['Success_Probability', 'Success_Class'], axis=1)
    y = df['Success_Probability']
    
    # Identify categorical and numerical columns
    categorical_cols = ['Industry', 'Revenue_Model', 'Competition_Level']
    numerical_cols = ['Team_Size', 'Market_Size_B', 'Innovation_Score', 'Marketing_Budget_k', 'Months_to_MVP']
    
    # Preprocessing pipelines
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Preprocessing data...")
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Build Neural Network
    model = Sequential([
        Dense(128, activation='relu', input_shape=(X_train_processed.shape[1],)),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid') # Predicting probability 0-1
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    print("Training model...")
    # Early stopping to prevent overfitting
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    history = model.fit(
        X_train_processed, y_train,
        validation_data=(X_test_processed, y_test),
        epochs=100,
        batch_size=32,
        callbacks=[early_stop],
        verbose=1
    )
    
    # Evaluate
    loss, mae = model.evaluate(X_test_processed, y_test, verbose=0)
    print(f"Test MAE: {mae:.4f}")
    
    # Save Model & Preprocessor
    os.makedirs('../../models', exist_ok=True)
    model.save('../../models/startup_success_model.h5')
    joblib.dump(preprocessor, '../../models/preprocessor.pkl')
    print("Saved TensorFlow model and preprocessor to models/")

if __name__ == '__main__':
    # Make sure we run from the correct directory relative to data/ and models/
    # Let's change dir to the script's dir
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_and_save_tf_model()
