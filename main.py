import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import os
import time
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Sagittal Infra Projects",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced user credentials with secure passwords
USER_CREDENTIALS = {
    "admin": {
        "password": "Sagittal@2024",
        "role": "admin",
        "office": "all"
    },
    "hyderabad": {
        "password": "Hyderabad@123",
        "role": "office_user",
        "office": "Hyderabad"
    },
    "jangareddygudem": {
        "password": "Jangareddy@123", 
        "role": "office_user",
        "office": "Jangareddygudem"
    },
    "annavaram": {
        "password": "Annavaram@123",
        "role": "office_user",
        "office": "Annavaram"
    },
    "rajamundry": {
        "password": "Rajamundry@123",
        "role": "office_user", 
        "office": "Rajamundry"
    },
    "koraput": {
        "password": "Koraput@123",
        "role": "office_user",
        "office": "Koraput"
    }
}

# Complete employee data with all Annavaram employees
EMPLOYEE_DATA = {
    "Hyderabad": ["Ramesh Kumar", "Suresh Reddy", "Priya Sharma", "Anil Gupta", "Rajesh Verma"],
    "Jangareddygudem": ["Mahesh Babu", "Lakshmi Devi", "Rajesh Kumar", "Sita Kumari"],
    "Annavaram": [
        "Mallela Srinivas", "GV Subba reddy", "M Ravi Kumar", "Tanneru Anusha", "P H Sai Ganesh",
        "M Pothiraj", "Yalamarthi V N S Lakshmi Durga", "Polugumati Sudev", "U Varalakshmi",
        "Gopisetti Teja", "Motukuri Srinu", "B Bobi", "Bodapati Raju", "Ravindra Reddy",
        "Narni Ganga Ramana", "Thirumala Giri Anil Gopi", "Munta Puthara Ganesh", "Gosu Ganesh",
        "Ponukumati Vijay Kumar", "Chelluboina Ravi Kumar", "Oleti Madhu", "M Madhu Babu",
        "Kolapati Ganga Chakradhar", "Chelluboina Ramakrishna", "Tanneru Saketh", 
        "Bogadhi Pradeep Kumar", "Bandaru Manoj Kumar", "Muppidi Simhachalam", "Y Suresh",
        "Gadde S P Pavan Kumar", "M Veera nageswara Rao", "Gundrra Swamy", "Nanhelal", "Angad",
        "Manish kumar", "R R Virendra Kumar", "Dhupathi Rajubabu", "Gokada Maharaj", 
        "Rongala Srinu", "Parupalli Srinu", "Bikas Kumar", "P Madhu Kumar", "CH Nani Babu",
        "Mayur", "Ashok Kumar Kushwaha", "B Nagendra", "Gampa Raju", "Altaf Raja", "Sohel",
        "Manoj Kumar", "Murali Krishna", "Kudrat Ali", "M Siva", "M Mahesh", 
        "Mummina Shyam Prasad", "Uppalapati Rama Chandra Rao", "Mummana Prasad", 
        "Yerra Srinivas", "Dasari Venkatesh", "Kandipalli Satyanarayana", "Ch Sunitha - Kodavali",
        "Ch Gangadhar-Kodavali", "Kotturu Nageswara Rao-BP", "Busala Paidiyya-BP",
        "Garllanka Nageswara rao-Garage", "Kakada chinnabbai-Arempudi", "D Chakravarthi - Garage",
        "Maddu Venkateswarulu - Arempudi", "M Apparao - Dharmavaram"
    ],
    "Rajamundry": ["Arun Kumar", "Madhavi Latha", "Pavan Kalyan", "Sravya Sri", "Kiran Reddy"],
    "Koraput": ["Biswa Ranjan", "Sunita Maharana", "Ajay Mishra", "Priyanka Das"]
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
        except Exception as e:
            st.error(f"Error loading data: {e}")
            self.data = {}
    
    def save_data(self):
        """Save attendance data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def mark_attendance(self, office: str, date_str: str, employee_data: List[dict]):
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

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user credentials"""
    if username in USER_CREDENTIALS:
        stored_password = USER_CREDENTIALS[username]["password"]
        if password == stored_password:
            return True
    return False

def get_user_role(username: str) -> dict:
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
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            color: #1f77b4;
            margin-bottom: 2rem;
        }
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<h1 class="main-header">🏗️ Sagittal Infra Projects</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Attendance Management System</h3>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.subheader("Login")
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    if authenticate_user(username, password):
                        user_info = get_user_role(username)
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_role = user_info["role"]
                        st.session_state.user_office = user_info["office"]
                        st.success(f"✅ Welcome {username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")

def admin_dashboard():
    """Admin dashboard - can view all offices"""
    st.title("👨‍💼 Admin Dashboard")
    st.subheader(f"Welcome Pavan - Sagittal Infra Projects")
    
    att_system = st.session_state.attendance_system
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 View Attendance", "📥 Download Reports", "📈 Analytics", "👥 Employee Info"])
    
    with tab1:
        st.subheader("Daily Attendance Overview")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_date = st.date_input("Select Date", date.today(), key="admin_view_date")  # ADDED UNIQUE KEY
            date_str = selected_date.strftime("%Y-%m-%d")
        
        # Quick stats
        offices_with_data = []
        total_employees = 0
        for office in EMPLOYEE_DATA.keys():
            if office in att_system.data and date_str in att_system.data[office]:
                offices_with_data.append(office)
                total_employees += len(att_system.data[office][date_str])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Offices Reported", f"{len(offices_with_data)}/5")
        with col2:
            st.metric("Total Employees", total_employees)
        with col3:
            st.metric("Date", selected_date.strftime("%d %b %Y"))
        
        # Display attendance data
        all_offices_data = []
        for office in EMPLOYEE_DATA.keys():
            if office in att_system.data and date_str in att_system.data[office]:
                for emp in att_system.data[office][date_str]:
                    emp_data = emp.copy()
                    emp_data['Office'] = office
                    emp_data['Date'] = date_str
                    all_offices_data.append(emp_data)
        
        if all_offices_data:
            df = pd.DataFrame(all_offices_data)
            df = df[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
            st.dataframe(df, use_container_width=True, height=400)
        else:
            st.info(f"📝 No attendance data available for {date_str}")
    
    with tab2:
        st.subheader("Generate Reports")
        
        col1, col2 = st.columns(2)
        with col1:
            report_type = st.selectbox("Report Type", ["Daily Report", "Monthly Report"], key="admin_report_type")
            office_filter = st.selectbox("Select Office", ["All Offices"] + list(EMPLOYEE_DATA.keys()), key="admin_office_filter")
        with col2:
            if report_type == "Daily Report":
                report_date = st.date_input("Select Date", date.today(), key="admin_report_date")  # ADDED UNIQUE KEY
                date_str = report_date.strftime("%Y-%m-%d")
            else:
                report_month = st.text_input("Enter Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key="admin_report_month")
        
        if st.button("🔄 Generate Report", type="primary", key="admin_generate_report"):
            with st.spinner("Generating report..."):
                if report_type == "Daily Report":
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
                    st.success("✅ Report generated successfully!")
                    df = df[['Date', 'Office', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    filename = f"sagittal_attendance_{office_filter}_{report_month if report_type == 'Monthly Report' else date_str}.csv"
                    
                    st.download_button(
                        label="📥 Download CSV Report",
                        data=csv,
                        file_name=filename,
                        mime="text/csv",
                        type="primary",
                        key="admin_download_report"
                    )
                else:
                    st.warning("📭 No data available for the selected criteria.")
    
    with tab3:
        st.subheader("Monthly Analytics")
        
        selected_month = st.text_input("Analysis Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key="admin_analytics_month")
        
        if st.button("📈 Generate Analytics", type="primary", key="admin_generate_analytics"):
            monthly_data = att_system.get_all_attendance(selected_month)
            
            if not monthly_data.empty:
                # Summary statistics
                st.subheader("Office-wise Summary")
                
                summary_data = []
                for office in monthly_data['Office'].unique():
                    office_data = monthly_data[monthly_data['Office'] == office]
                    total_records = len(office_data)
                    present_count = len(office_data[office_data['Status'] == 'Present'])
                    absent_count = len(office_data[office_data['Status'] == 'Absent'])
                    leave_count = len(office_data[office_data['Status'] == 'Leave'])
                    
                    summary_data.append({
                        'Office': office,
                        'Total Employees': len(EMPLOYEE_DATA[office]),
                        'Records': total_records,
                        'Present': present_count,
                        'Absent': absent_count,
                        'Leave': leave_count,
                        'Attendance %': f"{(present_count/total_records)*100:.1f}%" if total_records > 0 else "0%"
                    })
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)
            else:
                st.info(f"📊 No data available for {selected_month}")
    
    with tab4:
        st.subheader("Employee Information")
        
        for office, employees in EMPLOYEE_DATA.items():
            with st.expander(f"🏢 {office} - {len(employees)} Employees"):
                cols = st.columns(2)
                for i, employee in enumerate(employees):
                    with cols[i % 2]:
                        st.write(f"• {employee}")

def office_user_dashboard():
    """Office user dashboard - can only view/manage their office"""
    office_name = st.session_state.user_office
    st.title(f"🏢 {office_name} Office")
    st.subheader(f"Welcome {st.session_state.username}")
    
    att_system = st.session_state.attendance_system
    
    tab1, tab2, tab3 = st.tabs(["📝 Mark Attendance", "👀 View Records", "📤 Export Data"])
    
    with tab1:
        st.subheader("Mark Daily Attendance")
        
        selected_date = st.date_input("Select Date", date.today(), key=f"office_{office_name}_mark_date")
        date_str = selected_date.strftime("%Y-%m-%d")
        
        st.info(f"Marking attendance for **{selected_date.strftime('%d %B %Y')}** - {len(EMPLOYEE_DATA[office_name])} employees")
        
        # Check existing data
        existing_data = []
        if office_name in att_system.data and date_str in att_system.data[office_name]:
            st.warning("⚠️ Attendance already exists for today. You can update it.")
            existing_data = att_system.data[office_name][date_str]
        
        attendance_data = []
        
        # Create attendance form in batches to avoid overload
        batch_size = 10
        employees = EMPLOYEE_DATA[office_name]
        
        for batch_start in range(0, len(employees), batch_size):
            batch_end = min(batch_start + batch_size, len(employees))
            batch_employees = employees[batch_start:batch_end]
            
            with st.container():
                for i, employee_name in enumerate(batch_employees):
                    st.write(f"**{batch_start + i + 1}. {employee_name}**")
                    
                    col1, col2, col3 = st.columns([2, 1, 2])
                    
                    with col1:
                        default_status = 0
                        if existing_data:
                            for emp_data in existing_data:
                                if emp_data['Employee_Name'] == employee_name:
                                    default_status = ["Present", "Absent", "Leave", "Half-day"].index(emp_data['Status'])
                                    break
                        
                        status = st.selectbox(
                            f"Status for {employee_name}",
                            ["Present", "Absent", "Leave", "Half-day"],
                            key=f"status_{office_name}_{employee_name}_{batch_start}",
                            index=default_status,
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        default_time = "09:00"
                        if existing_data:
                            for emp_data in existing_data:
                                if emp_data['Employee_Name'] == employee_name:
                                    default_time = emp_data['In_Time']
                                    break
                        
                        in_time = st.text_input(
                            f"Time for {employee_name}",
                            value=default_time,
                            key=f"time_{office_name}_{employee_name}_{batch_start}",
                            placeholder="HH:MM",
                            label_visibility="collapsed",
                            disabled=(status != "Present")
                        )
                    
                    with col3:
                        default_remark = ""
                        if existing_data:
                            for emp_data in existing_data:
                                if emp_data['Employee_Name'] == employee_name:
                                    default_remark = emp_data.get('Remarks', '')
                                    break
                        
                        remarks = st.text_input(
                            f"Remarks for {employee_name}",
                            value=default_remark,
                            key=f"remarks_{office_name}_{employee_name}_{batch_start}",
                            placeholder="Remarks (optional)",
                            label_visibility="collapsed"
                        )
                    
                    attendance_data.append({
                        'Employee_Name': employee_name,
                        'Status': status,
                        'In_Time': in_time if status == "Present" else "",
                        'Remarks': remarks
                    })
                
                st.markdown("---")
        
        if st.button("💾 Save Attendance", type="primary", use_container_width=True, key=f"save_{office_name}"):
            # Validate times
            valid = True
            for emp in attendance_data:
                if emp['Status'] == 'Present' and emp['In_Time']:
                    try:
                        datetime.strptime(emp['In_Time'], '%H:%M')
                    except ValueError:
                        st.error(f"❌ Invalid time format for {emp['Employee_Name']}. Use HH:MM (24-hour)")
                        valid = False
                        break
            
            if valid:
                att_system.mark_attendance(office_name, date_str, attendance_data)
                st.success(f"✅ Attendance saved successfully for {date_str}!")
                time.sleep(1)
                st.rerun()
    
    with tab2:
        st.subheader("Attendance Records")
        
        view_date = st.date_input("Select Date", date.today(), key=f"office_{office_name}_view_date")
        date_str = view_date.strftime("%Y-%m-%d")
        
        if office_name in att_system.data and date_str in att_system.data[office_name]:
            df = pd.DataFrame(att_system.data[office_name][date_str])
            df['Date'] = date_str
            df['Office'] = office_name
            df = df[['Employee_Name', 'Status', 'In_Time', 'Remarks']]
            
            # Add summary
            present_count = len(df[df['Status'] == 'Present'])
            absent_count = len(df[df['Status'] == 'Absent'])
            leave_count = len(df[df['Status'] == 'Leave'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", len(df))
            col2.metric("Present", present_count)
            col3.metric("Absent", absent_count)
            col4.metric("Leave", leave_count)
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f"📝 No attendance records found for {view_date.strftime('%d %B %Y')}")
    
    with tab3:
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        with col1:
            report_type = st.selectbox("Report Type", ["Daily", "Monthly"], key=f"office_{office_name}_export_type")
        with col2:
            if report_type == "Daily":
                export_date = st.date_input("Select Date", date.today(), key=f"office_{office_name}_export_date")
                date_str = export_date.strftime("%Y-%m-%d")
            else:
                export_month = st.text_input("Enter Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key=f"office_{office_name}_export_month")
        
        if st.button("📊 Generate Export", type="primary", key=f"export_{office_name}"):
            if report_type == "Daily":
                df = att_system.get_office_attendance(office_name)
                df = df[df['Date'] == date_str]
            else:
                df = att_system.get_office_attendance(office_name, export_month)
            
            if not df.empty:
                st.success("✅ Export ready!")
                df = df[['Date', 'Employee_Name', 'Status', 'In_Time', 'Remarks']]
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False)
                file_suffix = date_str if report_type == "Daily" else export_month
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"attendance_{office_name}_{file_suffix}.csv",
                    mime="text/csv",
                    type="primary",
                    key=f"download_{office_name}"
                )
            else:
                st.warning("📭 No data available for export")

def main():
    """Main application function"""
    init_session_state()
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.title(f"👋 {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.user_role}")
        st.write(f"**Office:** {st.session_state.user_office}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content
    if st.session_state.user_role == "admin":
        admin_dashboard()
    else:
        office_user_dashboard()

if __name__ == "__main__":
    main()
