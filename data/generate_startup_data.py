import pandas as pd
import numpy as np
import random
import os

def generate_data(num_samples=5000):
    np.random.seed(42)
    random.seed(42)
    
    industries = ['SaaS', 'Fintech', 'Healthtech', 'Edtech', 'E-commerce', 'AI', 'Web3', 'Cybersecurity']
    revenue_models = ['B2B Subscription', 'B2C Subscription', 'Freemium', 'Marketplace', 'One-time Sales', 'Ad-supported']
    competition_levels = ['Low', 'Medium', 'High']
    
    data = {
        'Industry': np.random.choice(industries, num_samples),
        'Team_Size': np.random.randint(1, 100, num_samples),
        'Market_Size_B': np.random.uniform(0.1, 100.0, num_samples), # In billions
        'Revenue_Model': np.random.choice(revenue_models, num_samples),
        'Competition_Level': np.random.choice(competition_levels, num_samples),
        'Innovation_Score': np.random.randint(1, 11, num_samples),
        'Marketing_Budget_k': np.random.uniform(5, 500, num_samples),
        'Months_to_MVP': np.random.randint(1, 24, num_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate an artificial Success Probability
    # Weights for success
    success_score = np.zeros(num_samples)
    
    # Industry factor
    industry_weights = {'AI': 0.1, 'Fintech': 0.08, 'SaaS': 0.05, 'Healthtech': 0.07, 'Cybersecurity': 0.09, 'Edtech': 0.02, 'E-commerce': 0.01, 'Web3': 0.03}
    success_score += df['Industry'].map(industry_weights)
    
    # Team size (optimal 5-20)
    success_score += np.where((df['Team_Size'] >= 5) & (df['Team_Size'] <= 20), 0.1, 0)
    
    # Market size
    success_score += (df['Market_Size_B'] / 100.0) * 0.15
    
    # Innovation score
    success_score += (df['Innovation_Score'] / 10.0) * 0.25
    
    # Competition level
    comp_weights = {'Low': 0.1, 'Medium': 0.05, 'High': -0.05}
    success_score += df['Competition_Level'].map(comp_weights)
    
    # Months to MVP (faster is better)
    success_score += np.where(df['Months_to_MVP'] <= 6, 0.1, np.where(df['Months_to_MVP'] <= 12, 0.05, -0.05))
    
    # Add some random noise
    success_score += np.random.normal(0, 0.05, num_samples)
    
    # Normalize to 0-1
    success_score = (success_score - success_score.min()) / (success_score.max() - success_score.min())
    
    # Clip just in case
    df['Success_Probability'] = np.clip(success_score, 0, 1)
    
    # Classification targets (Success > 0.65)
    df['Success_Class'] = (df['Success_Probability'] > 0.65).astype(int)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/startups.csv', index=False)
    print(f"Generated {num_samples} samples and saved to data/startups.csv")

if __name__ == '__main__':
    generate_data()
