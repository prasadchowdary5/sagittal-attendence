import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import json
import hashlib
import os
from typing import Dict, List
import time

# Page configuration
st.set_page_config(
    page_title="Sagittal Infra Projects - Attendance System",
    page_icon="🏗️",
    layout="wide"
)

# User credentials (in production, use a proper database)
USER_CREDENTIALS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "office": "all"
    },
    "hyderabad_user": {
        "password": "hyderabad123",
        "role": "office_user",
        "office": "Hyderabad"
    },
    "jangareddygudem_user": {
        "password": "jangareddy123",
        "role": "office_user",
        "office": "Jangareddygudem"
    },
    "annavaram_user": {
        "password": "annavaram123",
        "role": "office_user",
        "office": "Annavaram"
    },
    "rajamundry_user": {
        "password": "rajamundry123",
        "role": "office_user",
        "office": "Rajamundry"
    },
    "koraput_user": {
        "password": "koraput123",
        "role": "office_user",
        "office": "Koraput"
    }
}

# Sample employee data for each office (You can replace this with your Excel data later)
EMPLOYEE_DATA = {
    "Hyderabad": ["Ramesh Kumar", "Suresh Reddy", "Priya Sharma", "Anil Gupta"],
    "Jangareddygudem": ["Mahesh Babu", "Lakshmi Devi", "Rajesh Kumar"],
    "Annavaram": ["Vikram Singh", "Geeta Patel", "Kiran Reddy", "Srinivas Rao"],
    "Rajamundry": ["Arun Kumar", "Madhavi Latha", "Pavan Kalyan", "Sravya Sri"],
    "Koraput": ["Biswa Ranjan", "Sunita Maharana", "Ajay Mishra"]
}


class AttendanceSystem:
    def __init__(self):
        self.data_file = "attendance_data.json"
        self.load_data()

    def load_data(self):
        """Load attendance data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            else:
                self.data = {}
        except:
            self.data = {}

    def save_data(self):
        """Save attendance data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def mark_attendance(self, office: str, date_str: str, employee_data: List[Dict]):
        """Mark attendance for an office on specific date"""
        if office not in self.data:
            self.data[office] = {}

        self.data[office][date_str] = employee_data
        self.save_data()

    def get_office_attendance(self, office: str, month: str = None):
        """Get attendance data for specific office"""
        if office not in self.data:
            return pd.DataFrame()

        all_data = []
        for date_str, employees in self.data[office].items():
            if month:
                if date_str.startswith(month):
                    for emp in employees:
                        emp_data = emp.copy()
                        emp_data['Date'] = date_str
                        emp_data['Office'] = office
                        all_data.append(emp_data)
            else:
                for emp in employees:
                    emp_data = emp.copy()
                    emp_data['Date'] = date_str
                    emp_data['Office'] = office
                    all_data.append(emp_data)

        return pd.DataFrame(all_data) if all_data else pd.DataFrame()

    def get_all_attendance(self, month: str = None):
        """Get all attendance data across all offices"""
        all_data = []
        for office in self.data:
            office_df = self.get_office_attendance(office, month)
            if not office_df.empty:
                all_data.append(office_df)

        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user credentials"""
    if username in USER_CREDENTIALS:
        stored_password = USER_CREDENTIALS[username]["password"]
        if password == stored_password:  # In production, use proper hashing
            return True
    return False


def get_user_role(username: str) -> Dict:
    """Get user role and office information"""
    return USER_CREDENTIALS.get(username, {})


def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_office' not in st.session_state:
        st.session_state.user_office = None
    if 'attendance_system' not in st.session_state:
        st.session_state.attendance_system = AttendanceSystem()


def login_page():
    """Login page for all users"""
    st.title("🏗️ Sagittal Infra Projects")
    st.subheader("Attendance Management System")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if authenticate_user(username, password):
                user_info = get_user_role(username)
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = user_info["role"]
                st.session_state.user_office = user_info["office"]
                st.success(f"Welcome {username}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")


def admin_dashboard():
    """Admin dashboard - can view all offices"""
    st.title("👨‍💼 Admin Dashboard")
    st.subheader(f"Welcome Pavan - Sagittal Infra Projects")

    # Initialize attendance system
    att_system = st.session_state.attendance_system

    # Tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 View All Attendance", "📥 Download Reports", "📈 Monthly Reports", "👥 Office Management"])

    with tab1:
        st.subheader("All Offices Attendance Data")

        # Date selector for admin
        selected_date = st.date_input("Select Date", date.today())
        date_str = selected_date.strftime("%Y-%m-%d")

        # View attendance for all offices on selected date
        all_offices_data = []
        for office in ["Hyderabad", "Jangareddygudem", "Annavaram", "Rajamundry", "Koraput"]:
            if office in att_system.data and date_str in att_system.data[office]:
                for emp in att_system.data[office][date_str]:
                    emp_data = emp.copy()
                    emp_data['Office'] = office
                    emp_data['Date'] = date_str
                    all_offices_data.append(emp_data)

        if all_offices_data:
            df = pd.DataFrame(all_offices_data)
            # Reorder columns for better readability
            df = df[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f"No attendance data available for {date_str}")

    with tab2:
        st.subheader("Download Attendance Reports")

        col1, col2 = st.columns(2)

        with col1:
            report_type = st.selectbox("Report Type", ["Daily Report", "Monthly Report"])
            office_filter = st.selectbox("Select Office", ["All Offices"] + list(EMPLOYEE_DATA.keys()))

        with col2:
            if report_type == "Daily Report":
                report_date = st.date_input("Select Date for Report", date.today())
            else:
                report_month = st.text_input("Enter Month (YYYY-MM)", value=date.today().strftime("%Y-%m"))

        if st.button("Generate Report"):
            if report_type == "Daily Report":
                date_str = report_date.strftime("%Y-%m-%d")
                if office_filter == "All Offices":
                    df = att_system.get_all_attendance()
                    df = df[df['Date'] == date_str]
                else:
                    df = att_system.get_office_attendance(office_filter)
                    df = df[df['Date'] == date_str]
            else:
                if office_filter == "All Offices":
                    df = att_system.get_all_attendance(report_month)
                else:
                    df = att_system.get_office_attendance(office_filter, report_month)

            if not df.empty:
                st.success("Report generated successfully!")
                # Reorder columns for better readability
                df = df[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
                st.dataframe(df, use_container_width=True)

                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"attendance_report_{office_filter}_{report_month if report_type == 'Monthly Report' else date_str}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for the selected criteria.")

    with tab3:
        st.subheader("Monthly Attendance Analysis")

        selected_month = st.text_input("Enter Month for Analysis (YYYY-MM)",
                                       value=date.today().strftime("%Y-%m"))

        if st.button("Generate Monthly Analysis"):
            monthly_data = att_system.get_all_attendance(selected_month)

            if not monthly_data.empty:
                # Summary statistics
                st.subheader("Monthly Summary")

                # Calculate attendance statistics
                summary_data = []
                for office in monthly_data['Office'].unique():
                    office_data = monthly_data[monthly_data['Office'] == office]
                    total_records = len(office_data)
                    present_count = len(office_data[office_data['Status'] == 'Present'])
                    absent_count = len(office_data[office_data['Status'] == 'Absent'])

                    summary_data.append({
                        'Office': office,
                        'Total Records': total_records,
                        'Present': present_count,
                        'Absent': absent_count,
                        'Attendance Rate': f"{(present_count / total_records) * 100:.1f}%"
                    })

                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)

                # Show detailed data
                st.subheader("Detailed Monthly Data")
                monthly_data = monthly_data[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
                st.dataframe(monthly_data, use_container_width=True)
            else:
                st.info(f"No data available for {selected_month}")

    with tab4:
        st.subheader("Office Employee Management")

        # Display current employee list for each office
        for office, employees in EMPLOYEE_DATA.items():
            with st.expander(f"{office} Office - {len(employees)} Employees"):
                for i, employee in enumerate(employees, 1):
                    st.write(f"{i}. {employee}")

        st.info("""
        **To update employee lists:**
        You can provide an Excel file with employee names for each office, 
        and the system will be updated accordingly.
        """)


def office_user_dashboard():
    """Office user dashboard - can only view/manage their office"""
    st.title(f"🏢 {st.session_state.user_office} Office Dashboard")
    st.subheader(f"Welcome {st.session_state.username}")

    att_system = st.session_state.attendance_system
    user_office = st.session_state.user_office

    tab1, tab2, tab3 = st.tabs(["📝 Mark Attendance", "📊 View Attendance", "📥 Download Reports"])

    with tab1:
        st.subheader("Mark Daily Attendance")

        selected_date = st.date_input("Select Date", date.today(), key="mark_date")
        date_str = selected_date.strftime("%Y-%m-%d")

        st.write(f"Marking attendance for: **{date_str}**")

        # Check if attendance already marked for today
        if user_office in att_system.data and date_str in att_system.data[user_office]:
            st.warning(f"Attendance already marked for {date_str}. You can update below.")
            existing_data = att_system.data[user_office][date_str]
        else:
            existing_data = []

        # Create attendance form
        attendance_data = []

        for i, employee_name in enumerate(EMPLOYEE_DATA[user_office]):
            st.write(f"**Employee:** {employee_name}")

            col1, col2 = st.columns([2, 1])

            with col1:
                # Set default status based on existing data or default to "Present"
                default_status = 0
                if existing_data:
                    for emp_data in existing_data:
                        if emp_data['Employee_Name'] == employee_name:
                            default_status = ["Present", "Absent", "Leave", "Half-day"].index(emp_data['Status'])
                            break

                status = st.selectbox(
                    f"Status for {employee_name}",
                    ["Present", "Absent", "Leave", "Half-day"],
                    key=f"status_{user_office}_{i}",
                    index=default_status
                )

            with col2:
                # Set default time based on existing data or default to 09:00
                default_time = "09:00"
                if existing_data:
                    for emp_data in existing_data:
                        if emp_data['Employee_Name'] == employee_name:
                            default_time = emp_data['In_Time']
                            break

                in_time = st.text_input(
                    f"In Time for {employee_name}",
                    value=default_time,
                    key=f"in_time_{user_office}_{i}",
                    placeholder="HH:MM (24hr)"
                )

            # Remarks field
            default_remark = ""
            if existing_data:
                for emp_data in existing_data:
                    if emp_data['Employee_Name'] == employee_name:
                        default_remark = emp_data.get('Remarks', '')
                        break

            remarks = st.text_input(
                f"Remarks for {employee_name}",
                value=default_remark,
                key=f"remarks_{user_office}_{i}",
                placeholder="Optional remarks"
            )

            st.markdown("---")

            attendance_data.append({
                'Employee_Name': employee_name,
                'Status': status,
                'In_Time': in_time,
                'Remarks': remarks
            })

        if st.button("Submit Attendance"):
            # Validate time format
            valid_times = True
            for emp_data in attendance_data:
                if emp_data['Status'] == 'Present' and emp_data['In_Time']:
                    try:
                        datetime.strptime(emp_data['In_Time'], '%H:%M')
                    except ValueError:
                        st.error(
                            f"Invalid time format for {emp_data['Employee_Name']}. Please use HH:MM format (24-hour).")
                        valid_times = False
                        break

            if valid_times:
                att_system.mark_attendance(user_office, date_str, attendance_data)
                st.success(f"Attendance marked successfully for {date_str}!")

    with tab2:
        st.subheader(f"View {user_office} Office Attendance")

        view_date = st.date_input("Select Date to View", date.today(), key="view_date")
        date_str = view_date.strftime("%Y-%m-%d")

        if user_office in att_system.data and date_str in att_system.data[user_office]:
            df = pd.DataFrame(att_system.data[user_office][date_str])
            df['Date'] = date_str
            df['Office'] = user_office
            # Reorder columns for better readability
            df = df[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f"No attendance data available for {date_str}")

    with tab3:
        st.subheader("Download Office Reports")

        col1, col2 = st.columns(2)

        with col1:
            report_type = st.selectbox("Report Type", ["Daily Report", "Monthly Report"], key="office_report")

        with col2:
            if report_type == "Daily Report":
                report_date = st.date_input("Select Date", date.today(), key="office_date")
                date_str = report_date.strftime("%Y-%m-%d")
            else:
                report_month = st.text_input("Enter Month (YYYY-MM)",
                                             value=date.today().strftime("%Y-%m"),
                                             key="office_month")

        if st.button("Generate Office Report"):
            if report_type == "Daily Report":
                df = att_system.get_office_attendance(user_office)
                df = df[df['Date'] == date_str]
            else:
                df = att_system.get_office_attendance(user_office, report_month)

            if not df.empty:
                st.success("Report generated successfully!")
                # Reorder columns for better readability
                df = df[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
                st.dataframe(df, use_container_width=True)

                # Download button
                csv = df.to_csv(index=False)
                file_suffix = date_str if report_type == "Daily Report" else report_month
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"attendance_{user_office}_{file_suffix}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for the selected criteria.")


def logout_button():
    """Logout button in sidebar"""
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.user_office = None
        st.rerun()


def main():
    """Main application function"""
    init_session_state()

    # Show login page if not authenticated
    if not st.session_state.authenticated:
        login_page()
        return

    # Show logout button in sidebar
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.user_role}")
    st.sidebar.write(f"Office: {st.session_state.user_office}")
    logout_button()

    # Route to appropriate dashboard based on role
    if st.session_state.user_role == "admin":
        admin_dashboard()
    else:
        office_user_dashboard()


if __name__ == "__main__":
    main()