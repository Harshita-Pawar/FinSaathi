import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Load Dataset
df = pd.read_csv('financial_data.csv')

print("=" * 50)
print("FINSAATHI - EXPLORATORY DATA ANALYSIS")
print("=" * 50)

print(f"\nDataset Shape: {df.shape}")
print(f"Total Users: {len(df)}")
print(f"\nFirst 5 rows:")
print(df.head())

print("\n--- Basic Statistics ---")
print(df.describe())

print("\n--- Missing Values ---")
print(df.isnull().sum())

# =====================
# EDA VISUALIZATIONS
# =====================

plt.style.use('dark_background')
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('FinSaathi - Financial Data Analysis', fontsize=16, color='white')

# 1. Income Distribution
axes[0, 0].hist(df['monthly_income'], bins=30, color='#00c6ff', edgecolor='black')
axes[0, 0].set_title('Income Distribution', color='white')
axes[0, 0].set_xlabel('Monthly Income (Rs.)', color='white')
axes[0, 0].set_ylabel('Count', color='white')
axes[0, 0].tick_params(colors='white')

# 2. Health Score Distribution
axes[0, 1].hist(df['health_score'], bins=20, color='#00ff88', edgecolor='black')
axes[0, 1].set_title('Health Score Distribution', color='white')
axes[0, 1].set_xlabel('Health Score', color='white')
axes[0, 1].set_ylabel('Count', color='white')
axes[0, 1].tick_params(colors='white')

# 3. Savings vs Income
axes[0, 2].scatter(df['monthly_income'], df['monthly_savings'],
                   alpha=0.5, color='#7b2ff7', s=10)
axes[0, 2].set_title('Savings vs Income', color='white')
axes[0, 2].set_xlabel('Monthly Income (Rs.)', color='white')
axes[0, 2].set_ylabel('Monthly Savings (Rs.)', color='white')
axes[0, 2].tick_params(colors='white')

# 4. Age vs Health Score
axes[1, 0].scatter(df['age'], df['health_score'],
                   alpha=0.5, color='#ff6b6b', s=10)
axes[1, 0].set_title('Age vs Health Score', color='white')
axes[1, 0].set_xlabel('Age', color='white')
axes[1, 0].set_ylabel('Health Score', color='white')
axes[1, 0].tick_params(colors='white')

# 5. Expense Breakdown Average
expense_cols = ['rent', 'food', 'transport', 'other_expenses']
avg_expenses = df[expense_cols].mean()
axes[1, 1].bar(expense_cols, avg_expenses,
               color=['#00c6ff', '#0072ff', '#7b2ff7', '#ff6b6b'])
axes[1, 1].set_title('Average Expense Breakdown', color='white')
axes[1, 1].set_xlabel('Category', color='white')
axes[1, 1].set_ylabel('Amount (Rs.)', color='white')
axes[1, 1].tick_params(colors='white')

# 6. Savings Rate Distribution
df['savings_rate'] = (df['monthly_savings'] / df['monthly_income']) * 100
axes[1, 2].hist(df['savings_rate'], bins=30, color='#ffaa00', edgecolor='black')
axes[1, 2].set_title('Savings Rate Distribution (%)', color='white')
axes[1, 2].set_xlabel('Savings Rate (%)', color='white')
axes[1, 2].set_ylabel('Count', color='white')
axes[1, 2].tick_params(colors='white')

plt.tight_layout()
plt.savefig('eda_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a')
print("\nEDA plots saved as eda_analysis.png!")

# =====================
# CORRELATION ANALYSIS
# =====================
print("\n--- Correlation Matrix ---")
corr = df[['age', 'monthly_income', 'total_expenses',
           'monthly_savings', 'health_score']].corr()
print(corr)

fig2, ax = plt.subplots(figsize=(8, 6), facecolor='#0a0a0a')
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax,
            linewidths=0.5, fmt='.2f')
ax.set_title('Correlation Heatmap', color='white', fontsize=14)
plt.savefig('correlation_heatmap.png', dpi=150,
            bbox_inches='tight', facecolor='#0a0a0a')
print("Correlation heatmap saved!")

# =====================
# ML MODEL TRAINING
# =====================
print("\n" + "=" * 50)
print("ML MODEL TRAINING & EVALUATION")
print("=" * 50)

# Features and Target
X = df[['age', 'monthly_income', 'rent', 'food', 'transport', 'other_expenses']]
y = df['monthly_savings']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation Metrics
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n--- Model Evaluation ---")
print(f"R² Score:              {r2:.4f}")
print(f"Mean Absolute Error:   Rs. {mae:,.0f}")
print(f"Model Accuracy:        {r2*100:.2f}%")

# Feature Importance
print(f"\n--- Feature Importance ---")
feature_names = ['Age', 'Income', 'Rent', 'Food', 'Transport', 'Other']
for name, coef in zip(feature_names, model.coef_):
    print(f"{name}: {coef:.2f}")

# Actual vs Predicted Plot
fig3, ax3 = plt.subplots(figsize=(8, 6), facecolor='#0a0a0a')
ax3.scatter(y_test, y_pred, alpha=0.5, color='#00c6ff', s=20)
ax3.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         'r--', linewidth=2, label='Perfect Prediction')
ax3.set_xlabel('Actual Savings (Rs.)', color='white')
ax3.set_ylabel('Predicted Savings (Rs.)', color='white')
ax3.set_title(f'Actual vs Predicted Savings\nR² = {r2:.4f} | MAE = Rs.{mae:,.0f}',
              color='white')
ax3.tick_params(colors='white')
ax3.legend(labelcolor='white')
plt.savefig('model_evaluation.png', dpi=150,
            bbox_inches='tight', facecolor='#0a0a0a')
print("\nModel evaluation plot saved!")

print("\n" + "=" * 50)
print("EDA COMPLETE!")
print(f"R² Score: {r2:.4f} — Model explains {r2*100:.2f}% of variance")
print("=" * 50)
