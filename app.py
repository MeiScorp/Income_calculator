import streamlit as st
import pandas as pd
import altair as alt

st.title("Income Calculator 💰")

# --- User Inputs ---
currency = st.selectbox("Currency:", ["EUR", "USD", "GBP", "UAH"])

salary = st.number_input("Monthly salary:", min_value=0.0, step=100.0)
tax_rate = st.slider("Tax rate (%):", 0, 50, 20)
extra_income = st.number_input("Extra monthly income:", min_value=0.0, step=50.0)
expenses = st.number_input("Monthly expenses:", min_value=0.0, step=50.0)

# --- Calculations ---
tax_amount = salary * (tax_rate / 100)
net_income = salary - tax_amount + extra_income - expenses

st.subheader("Monthly Summary")
st.write(f"**Tax amount:** {tax_amount:.2f} {currency}")
st.write(f"**Net monthly income:** {net_income:.2f} {currency}")

# --- Yearly Forecast ---
yearly_net = net_income * 12
st.subheader("Yearly Forecast")
st.write(f"**Estimated yearly net income:** {yearly_net:.2f} {currency}")

# --- Chart Data ---
df = pd.DataFrame({
    "Category": ["Salary", "Taxes", "Extra Income", "Expenses", "Net Income"],
    "Amount": [salary, -tax_amount, extra_income, -expenses, net_income]
})

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="Category",
        y="Amount",
        color="Category"
    )
    .properties(height=300)
)

st.subheader("Income & Expenses Chart")
st.altair_chart(chart, use_container_width=True)

# --- Save Results ---
st.subheader("Save Results")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Save this calculation"):
    st.session_state.history.append({
        "Salary": salary,
        "Tax rate": tax_rate,
        "Extra income": extra_income,
        "Expenses": expenses,
        "Net income": net_income,
        "Currency": currency
    })
    st.success("Saved!")

if st.session_state.history:
    st.write("### Saved Results")
    st.dataframe(pd.DataFrame(st.session_state.history))
