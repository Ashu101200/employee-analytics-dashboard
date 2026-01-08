import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Employee Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #e0f2fe, #bae6fd);
}

div[data-testid="metric-container"] {
    background-color: rgba(255, 255, 255, 0.35);
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("employee_data.csv")

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

department = st.sidebar.multiselect(
    "Select Department",
    options=df["DepartmentType"].dropna().unique(),
    default=df["DepartmentType"].dropna().unique()
)

status = st.sidebar.multiselect(
    "Employee Status",
    options=df["EmployeeStatus"].dropna().unique(),
    default=df["EmployeeStatus"].dropna().unique()
)

rating_range = st.sidebar.slider(
    "Performance Rating Range",
    float(df["Current Employee Rating"].min()),
    float(df["Current Employee Rating"].max()),
    (
        float(df["Current Employee Rating"].min()),
        float(df["Current Employee Rating"].max())
    )
)

if st.sidebar.button("🔄 Reset Filters"):
    st.experimental_rerun()

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["DepartmentType"].isin(department)) &
    (df["EmployeeStatus"].isin(status)) &
    (df["Current Employee Rating"].between(rating_range[0], rating_range[1]))
]

# ---------------- MAIN TITLE ----------------
st.title("📊 Employee Analytics Dashboard")
st.caption("Interactive HR Analytics Dashboard using Streamlit & Plotly")

# ---------------- KPI ROW ----------------
col1, col2, col3 = st.columns(3)

total_emp = len(filtered_df)
active_emp = len(filtered_df[filtered_df["EmployeeStatus"] == "Active"])
avg_rating = round(filtered_df["Current Employee Rating"].mean(), 2)

col1.metric("Total Employees", total_emp)
col2.metric("Active Employees", active_emp)
col3.metric("Avg Performance Rating", avg_rating)

st.divider()

# ---------------- CHART 1 ----------------
st.subheader("Employees by Department")

dept_count = filtered_df["DepartmentType"].value_counts().reset_index()
dept_count.columns = ["Department", "Employees"]

fig1 = px.bar(
    dept_count,
    x="Department",
    y="Employees",
    text="Employees",
    color="Department"
)
fig1.update_layout(transition_duration=600)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- CHART 2 ----------------
st.subheader("Performance Score Distribution")

perf_count = filtered_df["Performance Score"].value_counts().reset_index()
perf_count.columns = ["Performance Score", "Employees"]

fig2 = px.pie(
    perf_count,
    names="Performance Score",
    values="Employees",
    hole=0.4
)
fig2.update_layout(transition_duration=600)
st.plotly_chart(fig2, use_container_width=True)

# ---------------- CHART 3 ----------------
st.subheader("Employee Type Breakdown")

type_count = filtered_df["EmployeeType"].value_counts().reset_index()
type_count.columns = ["Employee Type", "Employees"]

fig3 = px.bar(
    type_count,
    x="Employee Type",
    y="Employees",
    text="Employees",
    color="Employee Type"
)
fig3.update_layout(transition_duration=600)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- CHART 4 ----------------
st.subheader("Average Performance Rating by Department")

dept_perf = (
    filtered_df
    .groupby("DepartmentType")["Current Employee Rating"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    dept_perf,
    x="DepartmentType",
    y="Current Employee Rating",
    text_auto=True,
    color="DepartmentType"
)
fig4.update_layout(transition_duration=600)
st.plotly_chart(fig4, use_container_width=True)

# ---------------- EMPLOYEE TABLE ----------------
st.subheader("Employee Details (Drill-Down View)")

st.dataframe(
    filtered_df[
        [
            "DepartmentType",
            "EmployeeStatus",
            "EmployeeType",
            "Current Employee Rating",
            "Performance Score"
        ]
    ],
    use_container_width=True
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("📌 Built using Streamlit & Plotly | HR Analytics Project")
