import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

from data.preprocess import load_data, clean_data, remove_outliers


# =========================
# LOAD + PREPROCESS DATA
# =========================
df = load_data("data/bengaluru_house_prices.csv")
df = clean_data(df)
df = remove_outliers(df)

# =========================
# FEATURE ENGINEERING (NO LEAKAGE)
# =========================
df['bath_per_bhk'] = df['bath'] / df['bhk']
df['total_rooms'] = df['bath'] + df['bhk']

# Handle any division issues
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

# =========================
# FEATURES & TARGET
# =========================
X = df[
    [
        'location',
        'total_sqft',
        'bath',
        'bhk',
        'bath_per_bhk',
        'total_rooms'
    ]
]

y = df['price']  # 🔥 NO LOG TRANSFORM

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# PREPROCESSOR
# =========================
num_features = [
    'total_sqft',
    'bath',
    'bhk',
    'bath_per_bhk',
    'total_rooms'
]

cat_features = ['location']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
])

# =========================
# MODEL (REGULARIZED)
# =========================
model = XGBRegressor(
    random_state=42,
    reg_alpha=0.1,
    reg_lambda=1
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model)
])

# =========================
# GRID SEARCH (OPTIMIZED)
# =========================
param_grid = {
    'model__n_estimators': [100, 150],
    'model__max_depth': [3, 4, 5],
    'model__learning_rate': [0.05, 0.1],
    'model__subsample': [0.8, 1],
    'model__colsample_bytree': [0.8, 1]
}

print("🔍 Running GridSearchCV...")

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=3,
    scoring='neg_mean_absolute_error',  # 🔥 real-world metric
    verbose=2,
    n_jobs=-1
)

grid.fit(X_train, y_train)

pipeline = grid.best_estimator_

print("✅ Best Params:", grid.best_params_)

# =========================
# EVALUATION
# =========================
print("📊 Evaluating model...")

y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ MAE: {mae:.2f}")
print(f"✅ R2 Score: {r2:.4f}")

# =========================
# SAVE MODEL
# =========================
with open("../backend/model/model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("💾 Model saved at: ../backend/model/model.pkl")