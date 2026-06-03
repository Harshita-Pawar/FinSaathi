import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import tempfile
import os

# Page Configuration
st.set_page_config(
    page_title="FinSaathi",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px !important;
    }
    h2 {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-top: 1rem !important;
    }
    h3 {
        color: #00c6ff !important;
        font-weight: 600 !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #00c6ff !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    .stTextInput label, .stNumberInput label {
        color: #aaaaaa !important;
        font-size: 0.9rem !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.4) !important;
    }
    div[data-testid="metric-container"] {
        background-color: #1a1a2e !important;
        border: 1px solid #00c6ff33 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    div[data-testid="metric-container"] label {
        color: #aaaaaa !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #00c6ff !important;
        font-weight: 700 !important;
    }
    hr {
        border-color: #222222 !important;
        margin: 2rem 0 !important;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    }
    p, span, div {
        color: #cccccc;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div style='text-align: center; padding: 3rem 0 2rem 0;'>
    <div style='font-size: 4rem; font-weight: 900; color: #ffffff; letter-spacing: -2px;'>
        💰 <span style='color: #ffffff;'>Fin</span><span style='color: #00c6ff;'>Saathi</span>
    </div>
    <div style='width: 80px; height: 4px; background: linear-gradient(90deg, #00c6ff, #0072ff); margin: 0.8rem auto;'></div>
    <p style='font-size: 1.3rem; color: #ffffff; font-weight: 600; margin-top: 0.5rem;'>
        Your Personal AI Finance Planner — Built for India
    </p>
    <p style='color: #aaaaaa; font-size: 0.95rem;'>Powered by Machine Learning & Financial Intelligence</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Initialize session state
if "calculated" not in st.session_state:
    st.session_state.calculated = False
if "savings" not in st.session_state:
    st.session_state.savings = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User Profile Section
st.markdown("## 👤 Tell Us About Yourself")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=18, max_value=60, value=25)
    monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=30000)
    current_savings = st.number_input("Current Total Savings (₹)", min_value=0, value=50000)
with col2:
    rent = st.number_input("Monthly Rent (₹)", min_value=0, value=5000)
    food = st.number_input("Monthly Food Expenses (₹)", min_value=0, value=3000)
    transport = st.number_input("Monthly Transport (₹)", min_value=0, value=2000)
    other = st.number_input("Other Expenses (₹)", min_value=0, value=2000)

st.markdown("---")

# AI Spending Prediction Inputs
st.markdown("## 🤖 AI Spending Prediction")
st.markdown("<p style='color: #aaaaaa;'>Enter your last 6 months expenses so our AI can predict your future spending!</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    m1 = st.number_input("Month 1 Expenses (₹)", min_value=0, value=12000)
    m2 = st.number_input("Month 2 Expenses (₹)", min_value=0, value=13000)
with col2:
    m3 = st.number_input("Month 3 Expenses (₹)", min_value=0, value=11500)
    m4 = st.number_input("Month 4 Expenses (₹)", min_value=0, value=14000)
with col3:
    m5 = st.number_input("Month 5 Expenses (₹)", min_value=0, value=13500)
    m6 = st.number_input("Month 6 Expenses (₹)", min_value=0, value=15000)

st.markdown("---")

# Functions
def calculate_health_score(income, expenses, savings):
    score = 0
    savings_rate = (savings / income) * 100 if income > 0 else 0
    if savings_rate >= 30: score += 40
    elif savings_rate >= 20: score += 30
    elif savings_rate >= 10: score += 20
    elif savings_rate > 0: score += 10
    expense_ratio = (expenses / income) * 100 if income > 0 else 100
    if expense_ratio <= 50: score += 40
    elif expense_ratio <= 60: score += 30
    elif expense_ratio <= 70: score += 20
    elif expense_ratio <= 80: score += 10
    if income >= 100000: score += 20
    elif income >= 50000: score += 15
    elif income >= 30000: score += 10
    elif income >= 15000: score += 5
    return score

def calculate_old_regime_tax(annual_income):
    if annual_income <= 250000: return 0
    elif annual_income <= 500000: return (annual_income - 250000) * 0.05
    elif annual_income <= 1000000: return 12500 + (annual_income - 500000) * 0.20
    else: return 112500 + (annual_income - 1000000) * 0.30

def calculate_new_regime_tax(annual_income):
    if annual_income <= 300000: return 0
    elif annual_income <= 600000: return (annual_income - 300000) * 0.05
    elif annual_income <= 900000: return 15000 + (annual_income - 600000) * 0.10
    elif annual_income <= 1200000: return 45000 + (annual_income - 900000) * 0.15
    elif annual_income <= 1500000: return 90000 + (annual_income - 1200000) * 0.20
    else: return 150000 + (annual_income - 1500000) * 0.30

def sip_recommender(age, savings):
    sip_amount = savings * 0.5
    if age <= 25:
        allocation = {"Large Cap": 30, "Mid Cap": 30, "Small Cap": 20, "ELSS": 20}
        risk = "Aggressive"
    elif age <= 35:
        allocation = {"Large Cap": 40, "Mid Cap": 25, "ELSS": 20, "Debt Funds": 15}
        risk = "Moderate"
    elif age <= 45:
        allocation = {"Large Cap": 40, "Debt Funds": 30, "ELSS": 15, "Gold Funds": 15}
        risk = "Conservative"
    else:
        allocation = {"Debt Funds": 50, "Large Cap": 25, "Gold Funds": 15, "Liquid Funds": 10}
        risk = "Very Conservative"
    return sip_amount, allocation, risk

def predict_spending(past_expenses):
    months = np.array(range(1, len(past_expenses) + 1)).reshape(-1, 1)
    expenses = np.array(past_expenses).reshape(-1, 1)
    model = LinearRegression()
    model.fit(months, expenses)
    prediction = model.predict(np.array([[len(past_expenses) + 1]]))[0][0]
    return prediction

def chatbot_response(question, income, expenses, savings, score, name):
    question = question.lower()
    if "health" in question or "score" in question:
        if score >= 70: return f"Your score is {score}/100 — Excellent! Keep it up {name}!"
        elif score >= 40: return f"Your score is {score}/100 — Average. Try saving more each month!"
        else: return f"Your score is {score}/100 — Poor. Reduce expenses and save at least 20% of income!"
    elif "save" in question or "saving" in question:
        rate = (savings / income * 100) if income > 0 else 0
        return f"You're saving Rs.{savings:,}/month ({rate:.1f}% of income). Aim for at least 20-30%!"
    elif "invest" in question or "sip" in question:
        if savings > 0: return f"Invest Rs.{savings*0.5:,.0f}/month in SIP. Start with Large Cap funds!"
        else: return "No savings to invest yet. Focus on reducing expenses first!"
    elif "afford" in question or "buy" in question:
        if savings > 5000: return f"You save Rs.{savings:,}/month. Ensure big purchases don't exceed 3 months of savings!"
        else: return f"Your savings of Rs.{savings:,}/month are low. Wait before making big purchases!"
    elif "tax" in question:
        old = calculate_old_regime_tax(income * 12)
        new = calculate_new_regime_tax(income * 12)
        better = "Old" if old < new else "New"
        return f"{better} Regime is better for you! Use 80C, 80D deductions to save more tax!"
    elif "emergency" in question:
        return f"Your 6-month emergency fund target is Rs.{expenses*6:,}. Keep it in a liquid fund!"
    elif "hi" in question or "hello" in question or "hey" in question:
        return f"Hello {name}! I am FinSaathi your AI finance assistant. Ask me anything!"
    elif "tip" in question or "advice" in question:
        import random
        tips = [
            "Save at least 20% of your income every month!",
            "Invest in ELSS to save tax under Section 80C!",
            "Always maintain a 6-month emergency fund!",
            "Start SIP early — Rs.500/month grows to lakhs in 10 years!",
            "Track your expenses weekly to avoid overspending!"
        ]
        return f"Finance Tip: {random.choice(tips)}"
    else:
        return f"Ask me about savings, investments, tax, emergency fund or health score {name}!"

plt.style.use('dark_background')

if st.button("⚡ Analyze My Finances"):
    st.session_state.calculated = True
    st.session_state.savings = monthly_income - (rent + food + transport + other)
    st.session_state.monthly_income = monthly_income
    st.session_state.total_expenses = rent + food + transport + other
    st.session_state.age = age
    st.session_state.name = name
    st.session_state.annual_income = monthly_income * 12
    st.session_state.rent = rent
    st.session_state.food = food
    st.session_state.transport = transport
    st.session_state.other = other
    st.session_state.current_savings = current_savings
    st.session_state.past_expenses = [m1, m2, m3, m4, m5, m6]

if st.session_state.calculated:
    savings = st.session_state.savings
    monthly_income = st.session_state.monthly_income
    total_expenses = st.session_state.total_expenses
    age = st.session_state.age
    name = st.session_state.name
    annual_income = st.session_state.annual_income
    rent = st.session_state.rent
    food = st.session_state.food
    transport = st.session_state.transport
    other = st.session_state.other
    current_savings = st.session_state.current_savings
    past_expenses = st.session_state.past_expenses
    score = calculate_health_score(monthly_income, total_expenses, savings)

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 16px; padding: 2rem; margin: 1rem 0; border: 1px solid #00c6ff33;'>
        <h2 style='color: #00c6ff; margin: 0;'>Hello, {name}! 👋</h2>
        <p style='color: #aaaaaa; margin: 0.5rem 0 0 0;'>Here's your complete financial analysis</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("💵 Monthly Income", f"₹{monthly_income:,}")
    with col2: st.metric("💸 Total Expenses", f"₹{total_expenses:,}")
    with col3: st.metric("💰 Monthly Savings", f"₹{savings:,}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Expense Breakdown")
        labels = ["Rent", "Food", "Transport", "Other", "Savings"]
        values = [rent, food, transport, other, savings]
        colors = ["#00c6ff", "#0072ff", "#7b2ff7", "#ff6b6b", "#00ff88"]
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#111111')
        ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90,
               textprops={'color': 'white', 'fontsize': 10})
        ax.set_facecolor('#111111')
        st.pyplot(fig)

    with col2:
        st.markdown("### 🏆 Financial Health Score")
        if score >= 70:
            score_color = "#00ff88"
            status = "Excellent"
            emoji = "🟢"
        elif score >= 40:
            score_color = "#ffaa00"
            status = "Average"
            emoji = "🟡"
        else:
            score_color = "#ff4444"
            status = "Poor"
            emoji = "🔴"
        st.markdown(f"""
        <div style='background: #1a1a2e; border-radius: 16px; padding: 2rem; text-align: center; border: 2px solid {score_color}; margin-top: 1rem;'>
            <div style='font-size: 4rem; font-weight: 900; color: {score_color};'>{score}</div>
            <div style='color: #aaaaaa; font-size: 1rem;'>out of 100</div>
            <div style='font-size: 1.5rem; margin-top: 0.5rem;'>{emoji} {status}</div>
            <div style='color: #aaaaaa; font-size: 0.85rem; margin-top: 0.5rem;'>
                {'Great job managing your finances!' if score >= 70 else 'Room for improvement!' if score >= 40 else 'Focus on reducing expenses!'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🧾 Tax Calculator — Old vs New Regime")
    old_tax = calculate_old_regime_tax(annual_income)
    new_tax = calculate_new_regime_tax(annual_income)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; border-radius: 12px; padding: 1.5rem; border: 1px solid #333;'>
            <h3 style='color: #aaaaaa;'>Old Regime</h3>
            <div style='font-size: 2rem; font-weight: 700; color: #00c6ff;'>₹{old_tax:,.0f}</div>
            <div style='color: #666;'>Annual Tax</div>
            <div style='color: #aaaaaa; margin-top: 0.5rem;'>₹{old_tax/12:,.0f} / month</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background: #1a1a2e; border-radius: 12px; padding: 1.5rem; border: 1px solid #333;'>
            <h3 style='color: #aaaaaa;'>New Regime</h3>
            <div style='font-size: 2rem; font-weight: 700; color: #7b2ff7;'>₹{new_tax:,.0f}</div>
            <div style='color: #666;'>Annual Tax</div>
            <div style='color: #aaaaaa; margin-top: 0.5rem;'>₹{new_tax/12:,.0f} / month</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if old_tax < new_tax:
        st.success(f"✅ Old Regime saves you ₹{new_tax - old_tax:,.0f} per year!")
    elif new_tax < old_tax:
        st.success(f"✅ New Regime saves you ₹{old_tax - new_tax:,.0f} per year!")
    else:
        st.info("Both regimes result in the same tax!")

    st.markdown("---")

    st.markdown("### 📈 SIP Investment Recommender")
    if savings > 0:
        sip_amount, allocation, risk = sip_recommender(age, savings)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background: #1a1a2e; border-radius: 12px; padding: 1.5rem; border: 1px solid #00c6ff33;'>
                <div style='color: #aaaaaa;'>Risk Profile</div>
                <div style='font-size: 1.5rem; font-weight: 700; color: #00c6ff;'>{risk}</div>
                <div style='color: #aaaaaa; margin-top: 1rem;'>Recommended SIP</div>
                <div style='font-size: 2rem; font-weight: 700; color: #00ff88;'>₹{sip_amount:,.0f}/month</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for fund, percent in allocation.items():
                amount = sip_amount * percent / 100
                st.markdown(f"**{fund}** — {percent}% → ₹{amount:,.0f}/month")
        with col2:
            fig2, ax2 = plt.subplots(figsize=(5, 5), facecolor='#111111')
            ax2.pie(list(allocation.values()), labels=list(allocation.keys()),
                    autopct="%1.1f%%", startangle=90,
                    colors=["#00c6ff", "#0072ff", "#7b2ff7", "#00ff88"],
                    textprops={'color': 'white', 'fontsize': 10})
            ax2.set_facecolor('#111111')
            st.pyplot(fig2)
    else:
        st.warning("⚠️ No savings available for SIP. Reduce expenses first!")

    st.markdown("---")

    st.markdown("### 🎯 Goal Planner")
    goal_name = st.text_input("What is your financial goal?", placeholder="e.g. Buy a Car, Emergency Fund, Vacation")
    goal_amount = st.number_input("How much do you need? (₹)", min_value=0, value=100000)
    goal_years = st.number_input("In how many years?", min_value=1, max_value=30, value=3)

    if st.button("Plan My Goal 🎯"):
        goal_months = goal_years * 12
        # Using compound interest formula for realistic calculation
        # Assuming 8% annual return on savings (FD/Debt fund rate)
        monthly_rate = 8 / 100 / 12
        if monthly_rate > 0:
            # SIP Future Value Formula: P * [((1+r)^n - 1) / r] * (1+r)
            monthly_needed = (goal_amount * monthly_rate) / ((1 + monthly_rate) ** goal_months - 1)
        else:
            monthly_needed = goal_amount / goal_months
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("🎯 Target", f"₹{goal_amount:,}")
        with col2: st.metric("📅 Timeline", f"{goal_years} Years")
        with col3: st.metric("💵 Monthly Needed (with 8% returns)", f"₹{monthly_needed:,.0f}")
        if monthly_needed <= savings:
            st.success(f"✅ Achievable! You'll still have ₹{savings - monthly_needed:,.0f} left monthly!")
        else:
            st.error(f"❌ You need ₹{monthly_needed - savings:,.0f} more per month!")
        months_list = list(range(1, int(goal_months) + 1))
        progress = [monthly_needed * m for m in months_list]
        fig3, ax3 = plt.subplots(facecolor='#111111')
        ax3.plot(months_list, progress, color="#00c6ff", linewidth=2)
        ax3.axhline(y=goal_amount, color="#00ff88", linestyle="--", label="Goal")
        ax3.fill_between(months_list, progress, alpha=0.2, color="#00c6ff")
        ax3.set_xlabel("Months", color='white')
        ax3.set_ylabel("Amount (₹)", color='white')
        ax3.set_title(f"Progress Towards {goal_name}", color='white')
        ax3.tick_params(colors='white')
        ax3.legend(labelcolor='white')
        st.pyplot(fig3)

    st.markdown("---")

    st.markdown("### 🚨 Emergency Fund Calculator")
    e3 = total_expenses * 3
    e6 = total_expenses * 6
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("💳 Current Savings", f"₹{current_savings:,}")
    with col2: st.metric("3️⃣ 3-Month Target", f"₹{e3:,}")
    with col3: st.metric("6️⃣ 6-Month Target", f"₹{e6:,}")
    if current_savings >= e6: st.success("✅ Fully funded 6-month emergency fund!")
    elif current_savings >= e3: st.warning(f"⚠️ Save ₹{e6 - current_savings:,} more for full coverage!")
    else: st.error(f"❌ Need ₹{e3 - current_savings:,} more for basic 3-month fund!")
    progress_pct = min(current_savings / e6 * 100, 100)
    st.markdown(f"**Emergency Fund: {progress_pct:.1f}% complete**")
    st.progress(int(progress_pct))
    months_left = (e6 - current_savings) / savings if savings > 0 and current_savings < e6 else 0
    if months_left > 0:
        st.info(f"💡 Complete in **{months_left:.0f} months** at current rate!")
    else:
        st.success("💡 Emergency fund complete! Focus on investing now!")

    st.markdown("---")

    st.markdown("### 🤖 AI Spending Prediction")
    prediction = predict_spending(past_expenses)
    avg_expense = sum(past_expenses) / len(past_expenses)
    trend = prediction - avg_expense
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📊 Avg Monthly Expense", f"₹{avg_expense:,.0f}")
    with col2: st.metric("🔮 Predicted Next Month", f"₹{prediction:,.0f}")
    with col3:
        if trend > 0: st.metric("📈 Trend", f"↑ ₹{trend:,.0f}", delta=f"+₹{trend:,.0f}")
        else: st.metric("📉 Trend", f"↓ ₹{abs(trend):,.0f}", delta=f"-₹{abs(trend):,.0f}")
    if prediction > monthly_income: st.error("🚨 Predicted expenses exceed income!")
    elif prediction > monthly_income * 0.8: st.warning("⚠️ Expenses quite high next month!")
    else: st.success("✅ Expenses look manageable next month!")
    fig4, ax4 = plt.subplots(facecolor='#111111')
    ax4.plot(range(1, 7), past_expenses, color="#00c6ff", linewidth=2, marker="o", label="Actual")
    ax4.plot(7, prediction, color="#ff6b6b", marker="*", markersize=15, label="Predicted")
    ax4.axhline(y=monthly_income, color="#00ff88", linestyle="--", label="Income")
    ax4.set_xlabel("Month", color='white')
    ax4.set_ylabel("Expenses (₹)", color='white')
    ax4.set_title("Spending Trend & AI Prediction", color='white')
    ax4.tick_params(colors='white')
    ax4.legend(labelcolor='white')
    st.pyplot(fig4)

    st.markdown("---")

    st.markdown("### 💬 FinSaathi AI Assistant")
    st.markdown("<p style='color: #aaaaaa;'>Ask me anything about your finances!</p>", unsafe_allow_html=True)
    user_question = st.text_input("💬 Your Question", placeholder="e.g. How is my financial health? Can I afford a phone?")
    if st.button("Ask FinSaathi 🤖"):
        if user_question:
            response = chatbot_response(user_question, monthly_income, total_expenses, savings, score, name)
            st.session_state.chat_history.append({"q": user_question, "a": response})
    if st.session_state.chat_history:
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"""
            <div style='background: #1a1a2e; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 3px solid #0072ff;'>
                <div style='color: #aaaaaa; font-size: 0.85rem;'>You</div>
                <div style='color: white;'>{chat['q']}</div>
            </div>
            <div style='background: #0d1117; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 3px solid #00c6ff;'>
                <div style='color: #00c6ff; font-size: 0.85rem;'>FinSaathi AI</div>
                <div style='color: #cccccc;'>{chat['a']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📄 Download Your Financial Report")
    st.markdown("<p style='color: #aaaaaa;'>Generate and download your complete financial report as PDF!</p>", unsafe_allow_html=True)
    if st.button("📥 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 20, "FinSaathi - Financial Report", ln=True, align="C")
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"Generated for: {name}", ln=True, align="C")
        pdf.ln(5)
        pdf.set_draw_color(0, 198, 255)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 10, "1. Financial Summary", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, f"Monthly Income:   Rs. {monthly_income:,}", ln=True)
        pdf.cell(0, 8, f"Total Expenses:   Rs. {total_expenses:,}", ln=True)
        pdf.cell(0, 8, f"Monthly Savings:  Rs. {savings:,}", ln=True)
        pdf.cell(0, 8, f"Current Savings:  Rs. {current_savings:,}", ln=True)
        pdf.ln(3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 10, "2. Financial Health Score", ln=True)
        pdf.set_font("Helvetica", "B", 20)
        if score >= 70:
            pdf.set_text_color(0, 200, 100)
            status_text = "Excellent"
        elif score >= 40:
            pdf.set_text_color(255, 170, 0)
            status_text = "Average"
        else:
            pdf.set_text_color(255, 68, 68)
            status_text = "Poor"
        pdf.cell(0, 12, f"{score}/100 - {status_text}", ln=True)
        pdf.ln(3)
        pdf.set_draw_color(0, 198, 255)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 10, "3. Tax Analysis", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, f"Old Regime Tax:  Rs. {old_tax:,.0f}", ln=True)
        pdf.cell(0, 8, f"New Regime Tax:  Rs. {new_tax:,.0f}", ln=True)
        better = "Old Regime" if old_tax < new_tax else "New Regime"
        pdf.cell(0, 8, f"Recommended:     {better}", ln=True)
        pdf.ln(3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 10, "4. SIP Recommendation", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        if savings > 0:
            sip_amount, allocation, risk = sip_recommender(age, savings)
            pdf.cell(0, 8, f"Risk Profile:        {risk}", ln=True)
            pdf.cell(0, 8, f"Monthly SIP Amount:  Rs. {sip_amount:,.0f}", ln=True)
            for fund, percent in allocation.items():
                amount = sip_amount * percent / 100
                pdf.cell(0, 7, f"  {fund}: {percent}% = Rs. {amount:,.0f}/month", ln=True)
        pdf.ln(3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 10, "5. Emergency Fund Status", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, f"6-Month Target:  Rs. {e6:,}", ln=True)
        pdf.cell(0, 8, f"Current Savings: Rs. {current_savings:,}", ln=True)
        pdf.cell(0, 8, f"Progress:        {progress_pct:.1f}%", ln=True)
        pdf.ln(3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 198, 255)
        pdf.cell(0, 10, "6. AI Spending Prediction", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, f"Predicted Next Month: Rs. {prediction:,.0f}", ln=True)
        if prediction > monthly_income:
            pdf.cell(0, 8, "Warning: Predicted expenses exceed income!", ln=True)
        else:
            pdf.cell(0, 8, "Status: Expenses look manageable!", ln=True)
        pdf.ln(5)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 8, "Generated by FinSaathi - AI-Based Personal Finance Planner", ln=True, align="C")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            st.download_button(
                label="📥 Click Here to Download Your Report",
                data=f,
                file_name=f"FinSaathi_Report_{name}.pdf",
                mime="application/pdf"
            )
        try:
            os.unlink(tmp.name)
        except:
            pass
        st.success("✅ Your PDF report is ready!")

    st.markdown("---")

    # Net Worth Tracker
    st.markdown("### 💎 Net Worth Tracker")
    st.markdown("<p style='color: #aaaaaa;'>Enter your assets and liabilities to calculate your net worth!</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Assets (What You Own)")
        bank_balance = st.number_input("Bank Balance (₹)", min_value=0, value=50000)
        investments = st.number_input("Investments & Mutual Funds (₹)", min_value=0, value=20000)
        gold = st.number_input("Gold Value (₹)", min_value=0, value=10000)
        property_value = st.number_input("Property Value (₹)", min_value=0, value=0)
        other_assets = st.number_input("Other Assets (₹)", min_value=0, value=0)
    with col2:
        st.markdown("#### Liabilities (What You Owe)")
        home_loan = st.number_input("Home Loan Outstanding (₹)", min_value=0, value=0)
        car_loan = st.number_input("Car Loan Outstanding (₹)", min_value=0, value=0)
        personal_loan = st.number_input("Personal Loan (₹)", min_value=0, value=0)
        credit_card = st.number_input("Credit Card Dues (₹)", min_value=0, value=0)
        other_liabilities = st.number_input("Other Liabilities (₹)", min_value=0, value=0)

    if st.button("Calculate Net Worth 💎"):
        total_assets = bank_balance + investments + gold + property_value + other_assets
        total_liabilities = home_loan + car_loan + personal_loan + credit_card + other_liabilities
        net_worth = total_assets - total_liabilities

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style='background: #1a1a2e; border-radius: 12px; padding: 1.5rem; text-align: center; border: 1px solid #00ff88;'>
                <div style='color: #aaaaaa;'>Total Assets</div>
                <div style='font-size: 1.8rem; font-weight: 700; color: #00ff88;'>₹{total_assets:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='background: #1a1a2e; border-radius: 12px; padding: 1.5rem; text-align: center; border: 1px solid #ff4444;'>
                <div style='color: #aaaaaa;'>Total Liabilities</div>
                <div style='font-size: 1.8rem; font-weight: 700; color: #ff4444;'>₹{total_liabilities:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            nw_color = "#00ff88" if net_worth >= 0 else "#ff4444"
            st.markdown(f"""
            <div style='background: #1a1a2e; border-radius: 12px; padding: 1.5rem; text-align: center; border: 2px solid {nw_color};'>
                <div style='color: #aaaaaa;'>Net Worth</div>
                <div style='font-size: 1.8rem; font-weight: 700; color: {nw_color};'>₹{net_worth:,}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if net_worth > 0:
            st.success(f"✅ Your net worth is positive at ₹{net_worth:,}! You own more than you owe!")
        elif net_worth == 0:
            st.warning("⚠️ Your net worth is zero. Focus on building assets!")
        else:
            st.error(f"❌ Your net worth is negative at ₹{net_worth:,}. Focus on clearing debts first!")

        col1, col2 = st.columns(2)
        with col1:
            fig5, ax5 = plt.subplots(facecolor='#111111')
            categories = ['Assets', 'Liabilities']
            values_nw = [total_assets, total_liabilities]
            colors_nw = ['#00ff88', '#ff4444']
            bars = ax5.bar(categories, values_nw, color=colors_nw, width=0.4)
            ax5.set_facecolor('#111111')
            ax5.set_ylabel('Amount (₹)', color='white')
            ax5.set_title('Assets vs Liabilities', color='white')
            ax5.tick_params(colors='white')
            for bar, val in zip(bars, values_nw):
                ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + total_assets*0.01,
                        f'₹{val:,}', ha='center', color='white', fontsize=9)
            st.pyplot(fig5)

        with col2:
            if total_assets > 0:
                fig6, ax6 = plt.subplots(facecolor='#111111')
                asset_labels = ['Bank', 'Investments', 'Gold', 'Property', 'Other']
                asset_values = [bank_balance, investments, gold, property_value, other_assets]
                asset_values_filtered = [(l, v) for l, v in zip(asset_labels, asset_values) if v > 0]
                if asset_values_filtered:
                    labels_f, values_f = zip(*asset_values_filtered)
                    ax6.pie(values_f, labels=labels_f, autopct='%1.1f%%', startangle=90,
                            colors=['#00c6ff', '#0072ff', '#7b2ff7', '#00ff88', '#ffaa00'],
                            textprops={'color': 'white', 'fontsize': 9})
                    ax6.set_facecolor('#111111')
                    ax6.set_title('Asset Breakdown', color='white')
                    st.pyplot(fig6)

        st.markdown("<br>", unsafe_allow_html=True)
        if net_worth > 10000000:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #0d2b1e, #1a1a2e); border-radius: 12px; padding: 1.5rem; border: 1px solid #00ff88;'>
                <div style='color: #00ff88; font-size: 1.2rem; font-weight: 700;'>Crorepati Status!</div>
                <div style='color: #aaaaaa;'>Your net worth exceeds Rs.1 Crore. Excellent financial position!</div>
            </div>
            """, unsafe_allow_html=True)
        elif net_worth > 5000000:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #0d2b1e, #1a1a2e); border-radius: 12px; padding: 1.5rem; border: 1px solid #00c6ff;'>
                <div style='color: #00c6ff; font-size: 1.2rem; font-weight: 700;'>50 Lakh+ Club!</div>
                <div style='color: #aaaaaa;'>Your net worth exceeds Rs.50 Lakhs. You are on your way to becoming a Crorepati!</div>
            </div>
            """, unsafe_allow_html=True)
        elif net_worth > 1000000:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 12px; padding: 1.5rem; border: 1px solid #00c6ff;'>
                <div style='color: #00c6ff; font-size: 1.2rem; font-weight: 700;'>Strong Financial Position!</div>
                <div style='color: #aaaaaa;'>Keep building your wealth. You are on the right track!</div>
            </div>
            """, unsafe_allow_html=True)
        elif net_worth > 0:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 12px; padding: 1.5rem; border: 1px solid #ffaa00;'>
                <div style='color: #ffaa00; font-size: 1.2rem; font-weight: 700;'>Building Wealth!</div>
                <div style='color: #aaaaaa;'>Good start! Focus on increasing investments and reducing liabilities.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #2b0d0d, #1a1a2e); border-radius: 12px; padding: 1.5rem; border: 1px solid #ff4444;'>
                <div style='color: #ff4444; font-size: 1.2rem; font-weight: 700;'>Focus on Debt Clearance!</div>
                <div style='color: #aaaaaa;'>Clear your liabilities first before building assets.</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #333333;'>
    <p>💰 FinSaathi — AI-Based Personal Finance Planner for Indian Users</p>
    <p style='font-size: 0.8rem;'>Built with Python, Streamlit & Machine Learning</p>
</div>
""", unsafe_allow_html=True)