import streamlit as st
import pandas as pd
import pickle
from decision_engine import decision_intelligence

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="AI Decision Intelligence – Customer Churn",
    layout="wide"
)

st.title("AI Decision Intelligence System – Customer Churn")
st.caption("Executive Decision Platform | Predict → Prioritize → Act")

st.markdown("""
This platform is designed for **management, retention, and business teams** to:
- Identify customers at risk of churn
- Understand *why* they are at risk
- Decide *what action* to take immediately
""")

# --------------------------------------------------
# Load model and features
# --------------------------------------------------
model = pickle.load(open("churn_model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

# --------------------------------------------------
# Upload section
# --------------------------------------------------
st.subheader("📂 Upload Customer Dataset")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # --------------------------------------------------
    # Encode categorical columns for model
    # --------------------------------------------------
    df["Contract"] = df["Contract"].map({
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    })

    df["InternetService"] = df["InternetService"].map({
        "DSL": 0,
        "Fiber optic": 1
    })

    X = df[features]

    # --------------------------------------------------
    # Churn prediction
    # --------------------------------------------------
    churn_prob = model.predict_proba(X)[:, 1] * 100
    df["Churn Probability (%)"] = churn_prob.round(2)

    # --------------------------------------------------
    # Decision intelligence layer
    # --------------------------------------------------
    risk_levels = []
    reasons = []
    primary_actions = []
    secondary_actions = []
    impacts = []

    for _, row in df.iterrows():
        rl, r, p, s, i = decision_intelligence(row, row["Churn Probability (%)"])
        risk_levels.append(rl)
        reasons.append(r)
        primary_actions.append(p)
        secondary_actions.append(s)
        impacts.append(i)

    df["Risk Level"] = risk_levels
    df["Why At Risk"] = reasons
    df["Primary Action"] = primary_actions
    df["Secondary Action"] = secondary_actions
    df["Business Impact"] = impacts

    # --------------------------------------------------
    # Sort by priority
    # --------------------------------------------------
    df = df.sort_values(by="Churn Probability (%)", ascending=False)

    # ==================================================
    # 📊 MANAGEMENT KPI SECTION
    # ==================================================
    st.subheader("📊 Management KPIs")

    total_customers = len(df)
    critical = (df["Risk Level"] == "Critical Risk").sum()
    moderate = (df["Risk Level"] == "Moderate Risk").sum()
    stable = (df["Risk Level"] == "Stable").sum()
    avg_risk = df["Churn Probability (%)"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", total_customers)
    col2.metric("Critical Risk Customers", critical)
    col3.metric("Moderate Risk Customers", moderate)
    col4.metric("Average Churn Probability", f"{avg_risk:.1f}%")

    # ==================================================
    # 📈 RISK DISTRIBUTION CHART (FIXED)
    # ==================================================
    st.subheader("📈 Risk Distribution Overview")

    risk_chart = df["Risk Level"].value_counts().reset_index()
    risk_chart.columns = ["Risk Level", "Customers"]

    st.bar_chart(
        risk_chart.set_index("Risk Level"),
        use_container_width=True
    )

    # ==================================================
    # 📉 CHURN PROBABILITY SPREAD
    # ==================================================
    st.subheader("📉 Churn Probability Spread")

    st.line_chart(
        df["Churn Probability (%)"].reset_index(drop=True),
        use_container_width=True
    )

    # ==================================================
    # 🧠 ACTION WORKLOAD INSIGHT
    # ==================================================
    st.subheader("🧠 Retention Action Workload")

    action_chart = df["Primary Action"].value_counts().reset_index()
    action_chart.columns = ["Action", "Customers"]

    st.bar_chart(
        action_chart.set_index("Action"),
        use_container_width=True
    )

    # ==================================================
    # 🚨 DECISION INTELLIGENCE PANEL
    # ==================================================
    st.subheader("🚨 Decision Intelligence Panel")
    st.write("Customers are ordered by urgency. Focus on **Critical Risk** first.")

    decision_view = df[
        [
            "Risk Level",
            "Churn Probability (%)",
            "Why At Risk",
            "Primary Action",
            "Secondary Action",
            "Business Impact"
        ]
    ]

    st.dataframe(decision_view, use_container_width=True)

    # ==================================================
    # 📥 DOWNLOAD REPORT
    # ==================================================
    st.download_button(
        label="⬇️ Download Executive Decision Report",
        data=df.to_csv(index=False),
        file_name="ai_decision_intelligence_churn_report.csv",
        mime="text/csv"
    )
