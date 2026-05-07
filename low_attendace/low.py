import pandas as pd
from datetime import datetime

df = pd.read_csv(
    "/home/aman/Desktop/attendance_python_automation_project/dataset/attendance_2023_2024.csv"
)


def calculate_hours(time_date):
    try:
        login_time, logout_time = time_date.split("-")
        login = datetime.strptime(login_time, "%H:%M")
        logout = datetime.strptime(logout_time, "%H:%M")
        total_time = logout - login
        hours = total_time.seconds / 3600
        return round(hours, 2)
    except:
        return 0


hours_report = pd.DataFrame()

# Add date column
hours_report["Date"] = df["Date"]

# process for each employee
for employee in df.columns[1:]:
    hours_report[employee] = df[employee].apply(calculate_hours)

# hours_report.to_excel("Working hours.xlsx")
# print("Done!!!")

low_attendance = pd.DataFrame()

low_attendance["Date"] = hours_report["Date"]

for employee in hours_report.columns[1:]:
    low_attendance[employee] = hours_report[employee].apply(
        lambda x: "Low Attendance" if x < 8 else "OK"
    )

# Save both the file in single excel file
with pd.ExcelWriter("attendace_report.xlsx") as writer:
    hours_report.to_excel(writer, sheet_name="Working hours report", index=False)
    low_attendance.to_excel(writer, sheet_name="Low Attendance report", index=False)

print("Completed")
