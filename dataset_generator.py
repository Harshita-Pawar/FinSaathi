import numpy as np
import pandas as pd

np.random.seed(42)
n = 1000

# Age between 22 and 55
age = np.random.randint(22, 55, n)

# Income based on age (older = higher income generally)
income = np.where(age < 30, np.random.randint(15000, 40000, n),
         np.where(age < 40, np.random.randint(30000, 80000, n),
         np.random.randint(50000, 150000, n)))

# Expenses as percentage of income
rent = (income * np.random.uniform(0.15, 0.35, n)).astype(int)
food = (income * np.random.uniform(0.08, 0.20, n)).astype(int)
transport = (income * np.random.uniform(0.05, 0.12, n)).astype(int)
other = (income * np.random.uniform(0.05, 0.15, n)).astype(int)

total_expenses = rent + food + transport + other
# Adding realistic noise to savings
noise = np.random.randint(-3000, 3000, n)
savings = income - total_expenses + noise
# Make sure savings doesn't go negative
savings = np.maximum(savings, 1000)


# Financial Health Score
health_score = []
for i in range(n):
    score = 0
    savings_rate = (savings[i] / income[i]) * 100
    if savings_rate >= 30: score += 40
    elif savings_rate >= 20: score += 30
    elif savings_rate >= 10: score += 20
    elif savings_rate > 0: score += 10
    expense_ratio = (total_expenses[i] / income[i]) * 100
    if expense_ratio <= 50: score += 40
    elif expense_ratio <= 60: score += 30
    elif expense_ratio <= 70: score += 20
    elif expense_ratio <= 80: score += 10
    if income[i] >= 100000: score += 20
    elif income[i] >= 50000: score += 15
    elif income[i] >= 30000: score += 10
    elif income[i] >= 15000: score += 5
    health_score.append(score)

# Create DataFrame
df = pd.DataFrame({
    'age': age,
    'monthly_income': income,
    'rent': rent,
    'food': food,
    'transport': transport,
    'other_expenses': other,
    'total_expenses': total_expenses,
    'monthly_savings': savings,
    'health_score': health_score
})

# Save to CSV
df.to_csv('financial_data.csv', index=False)
print(f"Dataset created with {len(df)} records!")
print(df.head())
print(df.describe())
