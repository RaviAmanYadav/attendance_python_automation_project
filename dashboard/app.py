import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attendance Dashbaord", layout="wide")
st.title("Attendace Dashboard")

df = pd.read_csv(
    "/home/aman/Desktop/attendance_python_automation_project/dataset/attendance_2023_2024.csv"
)

# Convert into date column
df["Date"] = pd.to_datetime(df["Date"])

# Employee
employees = df.columns[1:]

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📌 Dashboard Filters")

# Attendance threshold slider
attendance_threshold = st.sidebar.slider(
    "Attendance Threshold %", min_value=0, max_value=100, value=75
)

# Employee selector
selected_employee_sidebar = st.sidebar.selectbox("Select Employee", employees)

# Show raw dataset
show_raw_data = st.sidebar.checkbox("Show Raw Dataset")
# Function to calculate present


def isPresent(value):
    if pd.isna(value):
        return False

    value = str(value)

    return "-" in value


# calculate working hours
def calculate_hours(value):
    if not isPresent(value):
        return 0

    try:
        login, logout = value.split("-")
        login_time = pd.to_datetime(login)
        logout_time = pd.to_datetime(logout)
        hours = (logout_time - login_time).seconds / 3600
        return round(hours, 2)
    except:
        return 0


# Create summary
attendance_summary = []

official_login = pd.to_datetime("9:15")
official_logout = pd.to_datetime("17:00")

for employee in employees:
    present_day = 0
    total_hours = 0
    late_arrivals = 0
    early_logout = 0

    for value in df[employee]:

        # check attendance
        if isPresent(value):
            present_day += 1

            # working hours
            hours = calculate_hours(value)
            total_hours += hours

            # spliting time
            login, logout = value.split("-")
            login_time = pd.to_datetime(login)
            logout_time = pd.to_datetime(logout)

            # late arrivals
            if login_time > official_login:
                late_arrivals += 1

            # early logout check
            if logout_time < official_logout:
                early_logout += 1

    total_days = len(df)
    attendance_percentage = (present_day / total_days) * 100

    average_hours = total_hours / present_day if present_day > 0 else 0

    attendance_summary.append(
        {
            "Employee": employee,
            "Present Day": present_day,
            "Attendance Percentage": round(attendance_percentage, 2),
            "Average working hours": round(average_hours, 2),
            "Late Arrivals": late_arrivals,
            "Early logout": early_logout,
        }
    )

# Summary data fram
summary_df = pd.DataFrame(attendance_summary)

total_employee = len(employees)

average_attendance = summary_df["Attendance Percentage"].mean()

low_attendance = len(summary_df[summary_df["Attendance Percentage"] < 75])

# Top metric
col1, col2, col3 = st.columns(3)

col1.metric("Total Employee", total_employee)
col2.metric("Average Attendance", f"{average_attendance:.2f}%")
col3.metric("Below 75%", low_attendance)

st.divider()

# Show raw dataset

if show_raw_data:

    st.subheader("Raw Attendance Dataset")

    st.dataframe(df)

st.header("Employee summary")
st.dataframe(summary_df)
# Low attendance
st.subheader("Low Attendance")


low_df = summary_df[summary_df["Attendance Percentage"] < attendance_threshold]

st.dataframe(low_df)

# Search Employee
st.subheader("Employee Search")

# selected_employee = st.selectbox("Search employee", employees)
selected_employee = st.selectbox("Search employee", employees)

employee_df = pd.DataFrame({"Date": df["Date"], "Attendance": df[selected_employee]})
st.dataframe(employee_df)

# Bar chart
st.subheader("Average working hours")
fig2, ax2 = plt.subplots(figsize=(16, 6))
ax2.bar(summary_df["Employee"], summary_df["Average working hours"])

plt.xticks(rotation=90)
st.pyplot(fig2)

# Attendance percentage chart

st.subheader("Attendance Percentage")

fig3, ax3 = plt.subplots(figsize=(16, 6))
ax3.bar(summary_df["Employee"], summary_df["Attendance Percentage"], color="green")

plt.xticks(rotation=90)

st.pyplot(fig3)
