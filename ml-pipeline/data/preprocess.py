import pandas as pd
import numpy as np


def load_data(path):
    print("📥 Loading data...")
    return pd.read_csv(path)


def clean_data(df):
    print("🧹 Cleaning data...")

    # Drop irrelevant columns
    df = df.drop(columns=['society', 'availability'], errors='ignore')

    # Drop missing values
    df = df.dropna()

    # Convert size (e.g., "2 BHK" → 2)
    df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

    # Convert total_sqft
    def convert_sqft(x):
        try:
            if '-' in str(x):
                tokens = x.split('-')
                return (float(tokens[0]) + float(tokens[1])) / 2
            return float(x)
        except:
            return None

    df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
    df = df.dropna()

    # Remove invalid prices
    df = df[df['price'] > 0]

    # Clean location
    df['location'] = df['location'].apply(lambda x: x.strip())
    location_counts = df['location'].value_counts()

    df['location'] = df['location'].apply(
        lambda x: x if location_counts[x] > 10 else 'other'
    )

    # =========================
    # FEATURE ENGINEERING 🔥
    # =========================

    # Price per sqft
    df['price_per_sqft'] = (df['price'] * 100000) / df['total_sqft']

    # New engineered features
    df['bhk_per_sqft'] = df['bhk'] / df['total_sqft']
    df['bath_per_bhk'] = df['bath'] / df['bhk']
    df['total_rooms'] = df['bhk'] + df['bath']

    return df


def remove_outliers(df):
    print("🚫 Removing outliers...")

    # Price per sqft filtering
    df = df[(df['price_per_sqft'] > 1000) & (df['price_per_sqft'] < 30000)]

    # BHK sanity check
    df = df[df['total_sqft'] / df['bhk'] > 300]

    return df