def decision_intelligence(customer, risk_score):
    reasons = []
    primary_action = ""
    secondary_action = ""
    impact = ""

    if customer["tenure"] < 6:
        reasons.append("New customer with low engagement")

    if customer["MonthlyCharges"] > 80:
        reasons.append("High monthly cost sensitivity")

    if customer["Contract"] == 0:
        reasons.append("No long-term commitment")

    # Decision logic based on risk score
    if risk_score >= 70:
        risk_level = "Critical Risk"
        primary_action = "Immediate retention call with personalized offer"
        secondary_action = "Provide loyalty discount or plan downgrade"
        impact = "High probability of revenue loss if no action is taken"

    elif risk_score >= 40:
        risk_level = "Moderate Risk"
        primary_action = "Targeted engagement campaign"
        secondary_action = "Recommend contract upgrade incentives"
        impact = "Moderate churn risk, early intervention can improve retention"

    else:
        risk_level = "Stable"
        primary_action = "No immediate action required"
        secondary_action = "Monitor usage and satisfaction trends"
        impact = "Customer likely to remain active"

    return risk_level, ", ".join(reasons), primary_action, secondary_action, impact
