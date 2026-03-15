import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Shipping Route Efficiency", layout="wide")
st.markdown("""
<style>

.main {
    background-color: #F4F7FF;
}

h1, h2, h3 {
    color: #2A3F9D;
}

[data-testid="stMetricValue"] {
    color: #6A5ACD;
}

</style>
""", unsafe_allow_html=True)
col_logo1, col_logo2 = st.columns([1,5])
with col_logo1:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1sW7YHzFvzrhH9eAM2tdlhwbXB7SVq48B_g&s",
        width=120
    )
with col_logo2:
    st.image(
        "https://unifiedmentor.com/assets/Colored%20Logo-DMx5DaFN.png",
        width=250
    )
st.markdown("## 🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")
st.markdown("### Supply Chain Analytics | Unified Mentor Project")
df = pd.read_csv("processed_data.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min()
)
end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max()
)
region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)
state = st.sidebar.multiselect(
    "Select State",
    df["State/Province"].unique(),
    default=df["State/Province"].unique()
)
ship_mode = st.sidebar.multiselect(
    "Ship Mode",
    df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)
lead_threshold = st.sidebar.slider(
    "Lead Time Threshold (days)",
    0,20,5
)
filtered = df[
    (df["Order Date"] >= pd.to_datetime(start_date)) &
    (df["Order Date"] <= pd.to_datetime(end_date)) &
    (df["Region"].isin(region)) &
    (df["State/Province"].isin(state)) &
    (df["Ship Mode"].isin(ship_mode))
].copy()

filtered["Route"] = filtered["Factory"] + " → " + filtered["State/Province"]
st.subheader("📊 Key Metrics")
col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Shipments", len(filtered))
col2.metric(
    "Average Lead Time",
    round(filtered["Lead Time"].mean(),2)
)
col3.metric(
    "Total Sales",
    round(filtered["Sales"].sum(),2)
)
col4.metric(
    "Delayed Shipments",
    (filtered["Lead Time"] > lead_threshold).sum()
)
st.header("🚀 Route Efficiency Overview")
route_stats = filtered.groupby("Route").agg(
    Shipments=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean")
).reset_index()
leaderboard = route_stats.sort_values("Avg_Lead_Time")
fig1 = px.bar(
    leaderboard.head(10),
    x="Avg_Lead_Time",
    y="Route",
    orientation="h",
    color="Avg_Lead_Time",
    color_continuous_scale="Blues",
    title="Top Efficient Routes"
)

st.plotly_chart(fig1,use_container_width=True)

fig2 = px.bar(
    leaderboard.tail(10),
    x="Avg_Lead_Time",
    y="Route",
    orientation="h",
    color="Avg_Lead_Time",
    color_continuous_scale="Purples",
    title="Least Efficient Routes"
)

st.plotly_chart(fig2,use_container_width=True)
st.header("🌎 Geographic Shipping Map")
state_perf = filtered.groupby("State/Province").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipments=("Order ID","count")
).reset_index()
fig3 = px.choropleth(
    state_perf,
    locations="State/Province",
    locationmode="USA-states",
    color="Avg_Lead_Time",
    scope="usa",
    color_continuous_scale="PuBu",
    title="US Shipping Efficiency Heatmap"
)

st.plotly_chart(fig3,use_container_width=True)
region_perf = filtered.groupby("Region").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipments=("Order ID","count")
).reset_index()

fig4 = px.bar(
    region_perf,
    x="Region",
    y="Avg_Lead_Time",
    color="Region",
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="Regional Bottlenecks"
)

st.plotly_chart(fig4,use_container_width=True)
st.header("🚚 Ship Mode Comparison")

ship_perf = filtered.groupby("Ship Mode").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipments=("Order ID","count")
).reset_index()
fig5 = px.bar(
    ship_perf,
    x="Ship Mode",
    y="Avg_Lead_Time",
    color="Ship Mode",
    color_discrete_sequence=px.colors.sequential.Purples,
    title="Lead Time by Shipping Method"
)

st.plotly_chart(fig5,use_container_width=True)
st.header("🔍 Route Drill-Down")

selected_route = st.selectbox(
    "Select Route",
    filtered["Route"].unique()
)

route_data = filtered[
    filtered["Route"] == selected_route
]

state_analysis = route_data.groupby("State/Province").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipments=("Order ID","count")
).reset_index()

fig6 = px.bar(
    state_analysis,
    x="State/Province",
    y="Avg_Lead_Time",
    title="State-Level Route Performance",
    color="Avg_Lead_Time",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig6,use_container_width=True)
fig7 = px.line(
    route_data,
    x="Order Date",
    y="Lead Time",
    markers=True,
    title="Order Shipment Timeline"
)

st.plotly_chart(fig7,use_container_width=True)
st.subheader("Order Details")
st.dataframe(route_data)