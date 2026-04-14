import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup the Page Layout
st.set_page_config(page_title="EV Charging Algorithm Simulator", layout="wide")

st.title("⚡ EV Charging Algorithm Performance Simulation")
st.markdown("""
This dashboard compares different charging algorithms across six major cities. 
**Priority Order:** 1. CP Idle Time, 2. Total Wait Time, 3. Prosumer Idle Time.
""")

# 2. Data Organization
data = {
    "San Francisco": {
        "Algorithm": ["MinWaitMaxEarn", "FCFS", "Nearest", "NearestMaxDuration", "Reputation", "Greedy"],
        "Overall Avg Wait": [61.74, 53.02, 64.94, 74.86, 60.46, 63.15],
        "Prosumer Avg Wait": [4.05, 5.71, 3.65, 7.91, 5.20, 1.20],
        "Consumer Avg Wait": [119.44, 100.33, 126.22, 141.82, 115.73, 125.09],
        "CP Avg Down Time": [0.00, 11.08, 0.00, 1.09, 10.62, 1.58]
    },
    "Mexico City": {
        "Algorithm": ["MinWaitMaxEarn", "FCFS", "Nearest", "NearestMaxDuration", "Reputation", "Greedy"],
        "Overall Avg Wait": [14.07, 11.69, 13.30, 9.89, 12.24, 4.47],
        "Prosumer Avg Wait": [7.57, 10.80, 4.95, 9.20, 10.21, 1.86],
        "Consumer Avg Wait": [20.57, 12.59, 21.64, 10.58, 14.27, 7.08],
        "CP Avg Down Time": [22.08, 13.34, 47.82, 1.52, 13.91, 1.59]
    },
    "Beijing": {
        "Algorithm": ["MinWaitMaxEarn", "FCFS", "Nearest", "NearestMaxDuration", "Reputation", "Greedy"],
        "Overall Avg Wait": [8.36, 17.36, 7.71, 15.01, 10.84, 4.48],
        "Prosumer Avg Wait": [7.62, 11.34, 4.86, 9.21, 10.67, 1.89],
        "Consumer Avg Wait": [9.10, 23.38, 10.57, 20.81, 11.00, 7.08],
        "CP Avg Down Time": [0.03, 14.52, 0.04, 1.76, 15.18, 2.39]
    },
    "Mumbai": {
        "Algorithm": ["MinWaitMaxEarn", "FCFS", "Nearest", "NearestMaxDuration", "Reputation", "Greedy"],
        "Overall Avg Wait": [19.89, 12.63, 18.41, 30.45, 12.20, 5.30],
        "Prosumer Avg Wait": [9.48, 13.20, 6.30, 11.84, 12.10, 2.42],
        "Consumer Avg Wait": [30.30, 12.06, 30.52, 49.05, 12.29, 8.18],
        "CP Avg Down Time": [0.05, 16.15, 26.41, 2.19, 16.68, 2.89]
    },
    "Bangkok": {
        "Algorithm": ["MinWaitMaxEarn", "FCFS", "Nearest", "NearestMaxDuration", "Reputation", "Greedy"],
        "Overall Avg Wait": [27.90, 36.12, 26.90, 43.97, 34.19, 34.70],
        "Prosumer Avg Wait": [7.91, 11.04, 5.32, 10.30, 10.28, 2.00],
        "Consumer Avg Wait": [47.89, 61.19, 48.48, 77.63, 58.10, 67.40],
        "CP Avg Down Time": [0.02, 13.07, 0.02, 1.39, 13.07, 1.91]
    },
    "Cape Town": {
        "Algorithm": ["MinWaitMaxEarn", "FCFS", "Nearest", "NearestMaxDuration", "Reputation", "Greedy"],
        "Overall Avg Wait": [32.74, 20.18, 31.58, 33.64, 12.61, 28.33],
        "Prosumer Avg Wait": [8.85, 11.28, 6.44, 11.77, 10.39, 2.48],
        "Consumer Avg Wait": [56.63, 29.08, 56.73, 55.51, 14.82, 54.18],
        "CP Avg Down Time": [0.02, 10.67, 0.02, 1.56, 10.84, 1.80]
    }
}

# 3. Sidebar Selection
st.sidebar.header("Simulation Settings")
selected_city = st.sidebar.selectbox("Select City", list(data.keys()))

# 4. Data Preparation
df = pd.DataFrame(data[selected_city])
# Melting the data makes it easier for Plotly to create grouped bar charts
df_melted = df.melt(id_vars="Algorithm", var_name="Metric", value_name="Value")

# 5. Create Plot
fig = px.bar(
    df_melted, 
    x="Algorithm", 
    y="Value", 
    color="Metric", 
    barmode="group",
    title=f"Performance Comparison for {selected_city}",
    labels={"Value": "Time / Units", "Algorithm": "Charging Logic"},
    color_discrete_sequence=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']
)

fig.update_layout(hovermode="x unified", legend_title_text='Metric')

# 6. Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# 7. Add Analysis Table
st.subheader(f"Raw Data for {selected_city}")
st.dataframe(df.style.highlight_min(axis=0, color='lightgreen'))
