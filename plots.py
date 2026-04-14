import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="EV Allotment Analytics", layout="wide")

# 2. Data Organization
# Adding city-specific simulation parameters and compute times
city_meta = {
    "San Francisco": {"evs": 6000, "cps": 324, "compute_time": "4.01s"},
    "Mexico City": {"evs": 3000, "cps": 321, "compute_time": "1.39s"},
    "Beijing": {"evs": 3000, "cps": 319, "compute_time": "1.255s"},
    "Mumbai": {"evs": 3000, "cps": 315, "compute_time": "1.395s"},
    "Bangkok": {"evs": 3000, "cps": 314, "compute_time": "1.187s"},
    "Cape Town": {"evs": 3000, "cps": 314, "compute_time": "1.128s"}
}

city_data = {
    "San Francisco": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 61.74, "Prosumer Wait": 4.05, "Consumer Wait": 119.44, "CP Idle Time": 0.00},
        {"Algorithm": "FCFS", "Total Wait": 53.02, "Prosumer Wait": 5.71, "Consumer Wait": 100.33, "CP Idle Time": 11.08},
        {"Algorithm": "Nearest", "Total Wait": 64.94, "Prosumer Wait": 3.65, "Consumer Wait": 126.22, "CP Idle Time": 0.00},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 74.86, "Prosumer Wait": 7.91, "Consumer Wait": 141.82, "CP Idle Time": 1.09},
        {"Algorithm": "Reputation", "Total Wait": 60.46, "Prosumer Wait": 5.20, "Consumer Wait": 115.73, "CP Idle Time": 10.62},
        {"Algorithm": "Greedy", "Total Wait": 63.15, "Prosumer Wait": 1.20, "Consumer Wait": 125.09, "CP Idle Time": 1.58},
    ],
    "Mexico City": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 14.07, "Prosumer Wait": 7.57, "Consumer Wait": 20.57, "CP Idle Time": 22.08},
        {"Algorithm": "FCFS", "Total Wait": 11.69, "Prosumer Wait": 10.80, "Consumer Wait": 12.59, "CP Idle Time": 13.34},
        {"Algorithm": "Nearest", "Total Wait": 13.30, "Prosumer Wait": 4.95, "Consumer Wait": 21.64, "CP Idle Time": 47.82},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 9.89, "Prosumer Wait": 9.20, "Consumer Wait": 10.58, "CP Idle Time": 1.52},
        {"Algorithm": "Reputation", "Total Wait": 12.24, "Prosumer Wait": 10.21, "Consumer Wait": 14.27, "CP Idle Time": 13.91},
        {"Algorithm": "Greedy", "Total Wait": 4.47, "Prosumer Wait": 1.86, "Consumer Wait": 7.08, "CP Idle Time": 1.59},
    ],
    "Beijing": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 8.36, "Prosumer Wait": 7.62, "Consumer Wait": 9.10, "CP Idle Time": 0.03},
        {"Algorithm": "FCFS", "Total Wait": 17.36, "Prosumer Wait": 11.34, "Consumer Wait": 23.38, "CP Idle Time": 14.52},
        {"Algorithm": "Nearest", "Total Wait": 7.71, "Prosumer Wait": 4.86, "Consumer Wait": 10.57, "CP Idle Time": 0.04},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 15.01, "Prosumer Wait": 9.21, "Consumer Wait": 20.81, "CP Idle Time": 1.76},
        {"Algorithm": "Reputation", "Total Wait": 10.84, "Prosumer Wait": 10.67, "Consumer Wait": 11.00, "CP Idle Time": 15.18},
        {"Algorithm": "Greedy", "Total Wait": 4.48, "Prosumer Wait": 1.89, "Consumer Wait": 7.08, "CP Idle Time": 2.39},
    ],
    "Mumbai": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 19.89, "Prosumer Wait": 9.48, "Consumer Wait": 30.30, "CP Idle Time": 0.05},
        {"Algorithm": "FCFS", "Total Wait": 12.63, "Prosumer Wait": 13.20, "Consumer Wait": 12.06, "CP Idle Time": 16.15},
        {"Algorithm": "Nearest", "Total Wait": 18.41, "Prosumer Wait": 6.30, "Consumer Wait": 30.52, "CP Idle Time": 26.41},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 30.45, "Prosumer Wait": 11.84, "Consumer Wait": 49.05, "CP Idle Time": 2.19},
        {"Algorithm": "Reputation", "Total Wait": 12.20, "Prosumer Wait": 12.10, "Consumer Wait": 12.29, "CP Idle Time": 16.68},
        {"Algorithm": "Greedy", "Total Wait": 5.30, "Prosumer Wait": 2.42, "Consumer Wait": 8.18, "CP Idle Time": 2.89},
    ],
    "Bangkok": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 27.90, "Prosumer Wait": 7.91, "Consumer Wait": 47.89, "CP Idle Time": 0.02},
        {"Algorithm": "FCFS", "Total Wait": 36.12, "Prosumer Wait": 11.04, "Consumer Wait": 61.19, "CP Idle Time": 13.07},
        {"Algorithm": "Nearest", "Total Wait": 26.90, "Prosumer Wait": 5.32, "Consumer Wait": 48.48, "CP Idle Time": 0.02},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 43.97, "Prosumer Wait": 10.30, "Consumer Wait": 77.63, "CP Idle Time": 1.39},
        {"Algorithm": "Reputation", "Total Wait": 34.19, "Prosumer Wait": 10.28, "Consumer Wait": 58.10, "CP Idle Time": 13.07},
        {"Algorithm": "Greedy", "Total Wait": 34.70, "Prosumer Wait": 2.00, "Consumer Wait": 67.40, "CP Idle Time": 1.91},
    ],
    "Cape Town": [
        {"Algorithm": "MinWaitMaxEarn", "Total Wait": 32.74, "Prosumer Wait": 8.85, "Consumer Wait": 56.63, "CP Idle Time": 0.02},
        {"Algorithm": "FCFS", "Total Wait": 20.18, "Prosumer Wait": 11.28, "Consumer Wait": 29.08, "CP Idle Time": 10.67},
        {"Algorithm": "Nearest", "Total Wait": 31.58, "Prosumer Wait": 6.44, "Consumer Wait": 56.73, "CP Idle Time": 0.02},
        {"Algorithm": "NearestMaxDuration", "Total Wait": 33.64, "Prosumer Wait": 11.77, "Consumer Wait": 55.51, "CP Idle Time": 1.56},
        {"Algorithm": "Reputation", "Total Wait": 12.61, "Prosumer Wait": 10.39, "Consumer Wait": 14.82, "CP Idle Time": 10.84},
        {"Algorithm": "Greedy", "Total Wait": 28.33, "Prosumer Wait": 2.48, "Consumer Wait": 54.18, "CP Idle Time": 1.80},
    ]
}

# 3. Sidebar and Header
st.title("⚡ EV Allotment Analytics")
st.sidebar.header("Configuration")
selected_city = st.sidebar.selectbox("Select City", list(city_data.keys()))

# Display Simulation Metadata for the Selected City
meta = city_meta[selected_city]
st.markdown(f"""
### {selected_city} Simulation Environment
- **Total EVs:** {meta['evs']:,}
- **Total Charging Points (CPs):** {meta['cps']}
- **Compute Calculation Time:** `{meta['compute_time']}`
---
""")

st.sidebar.subheader("Metrics to Compare")
show_total = st.sidebar.checkbox("Total Wait", value=True)
show_prosumer = st.sidebar.checkbox("Prosumer Wait", value=False)
show_consumer = st.sidebar.checkbox("Consumer Wait", value=False)
show_idle = st.sidebar.checkbox("CP Idle Time", value=True)

selected_metrics = []
if show_total: selected_metrics.append("Total Wait")
if show_prosumer: selected_metrics.append("Prosumer Wait")
if show_consumer: selected_metrics.append("Consumer Wait")
if show_idle: selected_metrics.append("CP Idle Time")

if not selected_metrics:
    st.error("Please select at least one metric to visualize.")
    st.stop()

# 4. Calculation of Winners
df = pd.DataFrame(city_data[selected_city])
min_idle = df["CP Idle Time"].min()
winners_df = df[df["CP Idle Time"] == min_idle]
best_overall_row = winners_df.sort_values(by="Total Wait").iloc[0]
winner_names = ", ".join(winners_df["Algorithm"].tolist())

# 5. Key Metrics Visualization
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Infrastructure Winner(s)", winner_names)
with col2:
    st.metric("Lowest CP Idle Time", f"{min_idle:.2f} units")
with col3:
    st.metric("Top Winner Total Wait", f"{best_overall_row['Total Wait']:.2f} min")

# 6. Charting
df_plot = df[["Algorithm"] + selected_metrics]
df_melted = df_plot.melt(id_vars="Algorithm", var_name="Metric", value_name="Value")

fig = px.bar(
    df_melted, 
    x="Algorithm", 
    y="Value", 
    color="Metric", 
    barmode="group",
    title=f"Algorithmic Performance Comparison for {selected_city}",
    labels={"Value": "Time (Mins)"},
    color_discrete_map={
        "Total Wait": "#3b82f6",
        "Prosumer Wait": "#ef4444",
        "Consumer Wait": "#9333ea",
        "CP Idle Time": "#10b981"
    }
)
fig.update_layout(legend_title_text='Selected Metrics')
st.plotly_chart(fig, use_container_width=True)

# 7. Styled Data Table
st.subheader("Detailed Metric Breakdown")

def highlight_winners(s):
    is_winner = s["CP Idle Time"] == min_idle
    return ['background-color: rgba(16, 185, 129, 0.2)' if is_winner else '' for _ in s]

formatted_df = df[["Algorithm"] + selected_metrics]
st.dataframe(
    formatted_df.style.apply(highlight_winners, axis=1)
            .format({m: "{:.2f}" + ("m" if "Wait" in m else "") for m in selected_metrics})
            .highlight_min(subset=[m for m in selected_metrics if m == "CP Idle Time"], color="#10b981")
)
