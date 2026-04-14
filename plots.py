import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="EV Allotment Analytics", layout="wide")

# 2. Data Organization
city_data = {
    "San Francisco": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 61.74, "Prosumer Wait": 4.05, "CP Idle Time": 0.00},
        {"Algorithm": "FCFS", "Total Wait": 53.02, "Prosumer Wait": 5.71, "CP Idle Time": 11.08},
        {"Algorithm": "Nearest", "Total Wait": 64.94, "Prosumer Wait": 3.65, "CP Idle Time": 0.00},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 74.86, "Prosumer Wait": 7.91, "CP Idle Time": 1.09},
        {"Algorithm": "Reputation", "Total Wait": 60.46, "Prosumer Wait": 5.20, "CP Idle Time": 10.62},
        {"Algorithm": "Greedy", "Total Wait": 63.15, "Prosumer Wait": 1.20, "CP Idle Time": 1.58},
    ],
    "Mexico City": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 14.07, "Prosumer Wait": 7.57, "CP Idle Time": 22.08},
        {"Algorithm": "FCFS", "Total Wait": 11.69, "Prosumer Wait": 10.80, "CP Idle Time": 13.34},
        {"Algorithm": "Nearest", "Total Wait": 13.30, "Prosumer Wait": 4.95, "CP Idle Time": 47.82},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 9.89, "Prosumer Wait": 9.20, "CP Idle Time": 1.52},
        {"Algorithm": "Reputation", "Total Wait": 12.24, "Prosumer Wait": 10.21, "CP Idle Time": 13.91},
        {"Algorithm": "Greedy", "Total Wait": 4.47, "Prosumer Wait": 1.86, "CP Idle Time": 1.59},
    ],
    "Beijing": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 8.36, "Prosumer Wait": 7.62, "CP Idle Time": 0.03},
        {"Algorithm": "FCFS", "Total Wait": 17.36, "Prosumer Wait": 11.34, "CP Idle Time": 14.52},
        {"Algorithm": "Nearest", "Total Wait": 7.71, "Prosumer Wait": 4.86, "CP Idle Time": 0.04},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 15.01, "Prosumer Wait": 9.21, "CP Idle Time": 1.76},
        {"Algorithm": "Reputation", "Total Wait": 10.84, "Prosumer Wait": 10.67, "CP Idle Time": 15.18},
        {"Algorithm": "Greedy", "Total Wait": 4.48, "Prosumer Wait": 1.89, "CP Idle Time": 2.39},
    ],
    "Mumbai": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 19.89, "Prosumer Wait": 9.48, "CP Idle Time": 0.05},
        {"Algorithm": "FCFS", "Total Wait": 12.63, "Prosumer Wait": 13.20, "CP Idle Time": 16.15},
        {"Algorithm": "Nearest", "Total Wait": 18.41, "Prosumer Wait": 6.30, "CP Idle Time": 26.41},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 30.45, "Prosumer Wait": 11.84, "CP Idle Time": 2.19},
        {"Algorithm": "Reputation", "Total Wait": 12.20, "Prosumer Wait": 12.10, "CP Idle Time": 16.68},
        {"Algorithm": "Greedy", "Total Wait": 5.30, "Prosumer Wait": 2.42, "CP Idle Time": 2.89},
    ],
    "Bangkok": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 27.90, "Prosumer Wait": 7.91, "CP Idle Time": 0.02},
        {"Algorithm": "FCFS", "Total Wait": 36.12, "Prosumer Wait": 11.04, "CP Idle Time": 13.07},
        {"Algorithm": "Nearest", "Total Wait": 26.90, "Prosumer Wait": 5.32, "CP Idle Time": 0.02},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 43.97, "Prosumer Wait": 10.30, "CP Idle Time": 1.39},
        {"Algorithm": "Reputation", "Total Wait": 34.19, "Prosumer Wait": 10.28, "CP Idle Time": 13.07},
        {"Algorithm": "Greedy", "Total Wait": 34.70, "Prosumer Wait": 2.00, "CP Idle Time": 1.91},
    ],
    "Cape Town": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 32.74, "Prosumer Wait": 8.85, "CP Idle Time": 0.02},
        {"Algorithm": "FCFS", "Total Wait": 20.18, "Prosumer Wait": 11.28, "CP Idle Time": 10.67},
        {"Algorithm": "Nearest", "Total Wait": 31.58, "Prosumer Wait": 6.44, "CP Idle Time": 0.02},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 33.64, "Prosumer Wait": 11.77, "CP Idle Time": 1.56},
        {"Algorithm": "Reputation", "Total Wait": 12.61, "Prosumer Wait": 10.39, "CP Idle Time": 10.84},
        {"Algorithm": "Greedy", "Total Wait": 28.33, "Prosumer Wait": 2.48, "CP Idle Time": 1.80},
    ]
}

# 3. Sidebar and Header
st.title("⚡ EV Allotment Analytics")
st.markdown("### Priority: Minimizing CP Idle Time")

selected_city = st.sidebar.selectbox("Select City", list(city_data.keys()))

# 4. Calculation of Best Algorithm
df = pd.DataFrame(city_data[selected_city])
# Sort by CP Idle Time first, then Total Wait as a tie-breaker
best_row = df.sort_values(by=["CP Idle Time", "Total Wait"]).iloc[0]

# 5. Key Metrics Visualization
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Infrastructure Winner", best_row["Algorithm"])
with col2:
    st.metric("Lowest CP Idle Time", f"{best_row['CP Idle Time']:.2f} units")
with col3:
    st.metric("Associated Total Wait", f"{best_row['Total Wait']:.2f} min")

# 6. Charting
df_melted = df.melt(id_vars="Algorithm", var_name="Metric", value_name="Value")
fig = px.bar(
    df_melted, 
    x="Algorithm", 
    y="Value", 
    color="Metric", 
    barmode="group",
    title=f"Performance Comparison for {selected_city}",
    color_discrete_map={
        "Total Wait": "#3b82f6",
        "Prosumer Wait": "#ef4444",
        "CP Idle Time": "#10b981"  # Green for infrastructure
    }
)
fig.update_layout(legend_title_text='Metrics')
st.plotly_chart(fig, use_container_width=True)

# 7. Styled Data Table
st.subheader("Detailed Metric Breakdown")

def highlight_best_idle(s):
    is_best = s["CP Idle Time"] == best_row["CP Idle Time"]
    return ['background-color: rgba(16, 185, 129, 0.2)' if is_best else '' for _ in s]

# Applying styles to the table
st.dataframe(
    df.style.apply(highlight_best_idle, axis=1)
            .format({"Total Wait": "{:.2f}m", "Prosumer Wait": "{:.2f}m", "CP Idle Time": "{:.2f}"})
            .highlight_min(subset=["CP Idle Time"], color="#10b981")
)
