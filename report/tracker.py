import pandas as pd
from datetime import datetime

df = pd.read_csv(
    "/home/aman/Desktop/attendance_python_automation_project/dataset/attendance_2023_2024.csv"
)


# function to calculate hours of working
def calculate_hours(time_date):
    try:
        login, logout = time_date.split("-")
        login_time = datetime.strptime(login, "%H:%M")
        logout_time = datetime.strptime(logout, "%H:%M")
        total_time = logout_time - login_time
        hours = total_time.seconds / 3600
        return round(hours, 2)
    except:
        return 0


report = pd.DataFrame()

# add date column
report["Date"] = df["Date"]

# process each employee
for column in df.columns[1:]:
    report[column] = df[column].apply(calculate_hours)

# save report
report.to_excel("working_hours_report.xlsx")
print("Report Generate successfully")
