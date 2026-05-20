# frontend/app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ====================================
# SESSION STATE INIT
# ====================================

if "age" not in st.session_state:
    st.session_state.age = 30

if "total_working_years" not in st.session_state:
    st.session_state.total_working_years = 10

if "years_at_company" not in st.session_state:
    st.session_state.years_at_company = 5

if "years_with_curr_manager" not in st.session_state:
    st.session_state.years_with_curr_manager = 3

if "years_in_current_role" not in st.session_state:
    st.session_state.years_in_current_role = 3

if "years_since_last_promotion" not in st.session_state:
    st.session_state.years_since_last_promotion = 1

# ====================================
# AUTO VALIDATION LOGIC
# ====================================

def sync_working_years():

    max_working_years = max(
        st.session_state.age - 18,
        0
    )

    # clamp total working years
    st.session_state.total_working_years = min(
        st.session_state.total_working_years,
        max_working_years
    )

    # clamp company years
    st.session_state.years_at_company = min(
        st.session_state.years_at_company,
        st.session_state.total_working_years
    )
    sync_company_years()

def sync_company_years():

    max_company_years = (
        st.session_state.years_at_company
    )

    st.session_state.years_with_curr_manager = min(
        st.session_state.years_with_curr_manager,
        max_company_years
    )

    st.session_state.years_in_current_role = min(
        st.session_state.years_in_current_role,
        max_company_years
    )

    st.session_state.years_since_last_promotion = min(
        st.session_state.years_since_last_promotion,
        max_company_years
    )

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:5000"

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Employee Database",
        "Manual Prediction"
    ]
)

# ====================================
    # DASHBOARD PAGE
# ====================================

if page == "Dashboard":

    st.title("Employee Attrition Dashboard")

    COLOR_PURPLE = "#6366F1"
    COLOR_HIGH = "#EF4444"
    COLOR_MEDIUM = "#F59E0B"
    COLOR_LOW = "#10B981"

    st.markdown("""
            <style>
            div[data-testid="stMetric"] {
                background-color: var(--background-secondary-color) !important;
                padding: 15px 20px;
                border-radius: 10px;
                border: 2px solid var(--text-color) !important;
                box-shadow: none !important;
            }
            
            div[data-testid="stMetric"] label, 
            div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
                color: var(--text-color) !important;
            }
            </style>
        """, unsafe_allow_html=True)

    try:
        response_summary = requests.get(f"{BACKEND_URL}/dashboard/summary")
        response_trends = requests.get(f"{BACKEND_URL}/dashboard/trends")

        if response_summary.status_code == 200:
            summary = response_summary.json()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Employees", summary["total_employees"])
            with col2:
                st.metric("High Risk Employees", summary["high_risk_count"])
            with col3:
                med_mock = int(summary["total_employees"] * 0.2)
                st.metric("Medium Risk", med_mock)
            with col4:
                st.metric("Attrition Rate", f'{summary["attrition_rate"]}%')

            st.markdown(" ")

            chart_col1, chart_col2 = st.columns([2, 1])

            with chart_col1:
                st.subheader("Attrition By Department")

                if response_trends.status_code == 200:
                    trends_res = response_trends.json()

                    if trends_res.get("success") and trends_res.get("data"):
                        df_trends = pd.DataFrame(trends_res["data"])

                        fig_bar = px.bar(
                            df_trends,
                            x="Department",
                            y="attrition_count",
                            color_discrete_sequence=[COLOR_PURPLE],
                            labels={"Department": "Department", "attrition_count": "Attrition Count"}
                        )

                        fig_bar.update_layout(
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=20, r=20, t=20, b=20),
                            xaxis={'categoryorder': 'total descending'}
                        )
                        fig_bar.update_yaxes(showgrid=True, gridcolor="#F1F5F9")

                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.info("No trend data available.")
                else:
                    st.error("Failed to load department trends from API.")

            with chart_col2:
                st.subheader("Risk Distribution")

                high_count = summary["high_risk_count"]
                total_count = summary["total_employees"]

                med_count = int(total_count * 0.2)
                low_count = max(total_count - high_count - med_count, 0)

                df_donut = pd.DataFrame({
                    "Risk Level": ["High", "Medium", "Low"],
                    "Count": [high_count, med_count, low_count]
                })

                fig_donut = px.pie(
                    df_donut,
                    values="Count",
                    names="Risk Level",
                    hole=0.6,
                    color="Risk Level",
                    color_discrete_map={
                        "High": COLOR_HIGH,
                        "Medium": COLOR_MEDIUM,
                        "Low": COLOR_LOW
                    }
                )

                fig_donut.update_layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )

                st.plotly_chart(fig_donut, use_container_width=True)

                # ====================================
                # CRITICAL ACTION REQUIRED
                # ====================================
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("Critical Action Required")

                st.markdown("""
                    <style>
                    .employee-risk-card {
                        background-color: white;
                        padding: 12px 16px;
                        border-radius: 8px;
                        border: 1px solid #E2E8F0;
                        margin-bottom: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        box-shadow: 0px 2px 5px rgba(0,0,0,0.02);
                    }
                    .emp-info {
                        display: flex;
                        align-items: center;
                        gap: 12px;
                    }
                    .emp-avatar {
                        width: 36px;
                        height: 36px;
                        background-color: #E2E8F0;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        color: #64748B;
                        font-size: 14px;
                    }
                    .emp-name {
                        font-weight: 600;
                        color: #1E293B;
                        font-size: 14px;
                        margin: 0;
                    }
                    .emp-role {
                        color: #64748B;
                        font-size: 12px;
                        margin: 0;
                    }
                    .risk-badge {
                        background-color: #FEE2E2;
                        color: #EF4444;
                        padding: 4px 8px;
                        border-radius: 6px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    </style>
                """, unsafe_allow_html=True)

                try:
                    response_emp = requests.get(f"{BACKEND_URL}/employees")
                    if response_emp.status_code == 200:
                        emp_list = response_emp.json().get("employees", [])

                        # Bảo mật logic kiểm tra chữ hoa/thường cho risk_level
                        high_risk_employees = [e for e in emp_list if
                                               str(e.get("risk_level")).strip().capitalize() == "High"][:4]

                        if high_risk_employees:
                            for emp in high_risk_employees:
                                first_letter = emp['employee_name'][0] if emp['employee_name'] else "E"
                                job_role_str = emp.get('JobRole', emp.get('job_role', 'Staff'))
                                dept_str = emp.get('Department', emp.get('department', 'N/A'))

                                st.markdown(f"""
                                    <div class="employee-risk-card">
                                        <div class="emp-info">
                                            <div class="emp-avatar">{first_letter}</div>
                                            <div>
                                                <p class="emp-name">{emp['employee_name']}</p>
                                                <p class="emp-role">{job_role_str} - {dept_str}</p>
                                            </div>
                                        </div>
                                        <div class="risk-badge">High Risk</div>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.success("Safe! No High Risk employees detected.")
                    else:
                        st.write("Unable to fetch real-time critical actions.")
                except Exception as e:
                    st.write(f"Style handling error: {str(e)}")

        else:
            st.error("Failed to load dashboard summary")

    except Exception as e:
        st.error(f"Error rendering charts: {str(e)}")
# ====================================
# EMPLOYEE DATABASE PAGE
# ====================================

elif page == "Employee Database":

    st.title(
        "Employee Database"
    )

    try:

        response = requests.get(
            f"{BACKEND_URL}/employees"
        )

        if response.status_code == 200:

            result = response.json()

            employees = result[
                "employees"
            ]

            df = pd.DataFrame(
                employees
            )

            st.subheader(
                "Employee Table"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # ====================================
            # EMPLOYEE SELECT
            # ====================================

            employee_ids = (

                df["EmployeeNumber"]

                .tolist()
            )

            selected_employee_id = (

                st.selectbox(

                    "Select Employee ID",

                    employee_ids
                )
            )

            selected_employee = df[

                df["EmployeeNumber"]

                == selected_employee_id

            ].iloc[0]

            # ====================================
            # EMPLOYEE DETAIL
            # ====================================

            st.subheader(
                "Employee Detail"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(

                    f"Name: "

                    f"{selected_employee['employee_name']}"
                )

                st.write(

                    f"Department: "

                    f"{selected_employee['Department']}"
                )

                st.write(

                    f"Role: "

                    f"{selected_employee['JobRole']}"
                )

                st.write(

                    f"Risk Level: "

                    f"{selected_employee['risk_level']}"
                )

            with col2:

                st.write(

                    f"Email: "

                    f"{selected_employee['email']}"
                )

                st.write(

                    f"Age: "

                    f"{selected_employee['Age']}"
                )

                st.write(

                    f"Monthly Income: "

                    f"{selected_employee['MonthlyIncome']}"
                )

                st.write(

                    f"Years At Company: "

                    f"{selected_employee['YearsAtCompany']}"
                )

            st.divider()

            # ====================================
            # RUN PREDICTION
            # ====================================

            if st.button(
                "Run Employee Prediction"
            ):

                with st.spinner(
                    "Predicting..."
                ):

                    prediction_response = (

                        requests.post(

                            f"{BACKEND_URL}/predict/{selected_employee_id}"
                        )
                    )

                    if (
                        prediction_response.status_code
                        == 200
                    ):

                        result = (
                            prediction_response.json()
                        )

                        if result["success"]:

                            st.subheader(
                                "Prediction Result"
                            )

                            probability = (

                                result[
                                    "attrition_probability"
                                ]
                            )

                            risk_level = (

                                result[
                                    "risk_level"
                                ]
                            )

                            st.write(

                                f"Attrition Probability: "

                                f"{probability * 100:.2f}%"
                            )

                            if risk_level == "High":

                                st.error(

                                    f"Risk Level: "

                                    f"{risk_level}"
                                )

                            elif risk_level == "Medium":

                                st.warning(

                                    f"Risk Level: "

                                    f"{risk_level}"
                                )

                            else:

                                st.success(

                                    f"Risk Level: "

                                    f"{risk_level}"
                                )

                        else:

                            st.error(
                                result["error"]
                            )

                    else:

                        st.error(
                            "Prediction failed"
                        )

        else:

            st.error(
                "Failed to load employees"
            )

    except Exception as e:

        st.error(str(e))

# ====================================
# MANUAL PREDICTION PAGE
# ====================================

elif page == "Manual Prediction":

    st.title(
        "Manual Employee Prediction"
    )

    st.subheader(
        "Employee Information"
    )

    col1, col2 = st.columns(2)

    # ====================================
    # LEFT COLUMN
    # ====================================

    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=65,
            value=30
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=1000,
            value=5000
        )

        # ====================================
        # WORKING YEARS LOGIC
        # ====================================

        max_working_years = max(
            age - 18,
            0
        )

        total_working_years = st.number_input(
            "Total Working Years",
            min_value=0,
            max_value=max_working_years,
            value=min(10, max_working_years)
        )

        years_at_company = st.number_input(
            "Years At Company",
            min_value=0,
            max_value=total_working_years,
            value=min(5, total_working_years)
        )

        years_with_curr_manager = st.number_input(
            "Years With Current Manager",
            min_value=0,
            max_value=years_at_company,
            value=min(3, years_at_company)
        )

        years_in_current_role = st.number_input(
            "Years In Current Role",
            min_value=0,
            max_value=years_at_company,
            value=min(3, years_at_company)
        )

        years_since_last_promotion = st.number_input(
            "Years Since Last Promotion",
            min_value=0,
            max_value=total_working_years,
            value=min(1, total_working_years)
        )

        # ====================================
        # BASIC HR FEATURES
        # ====================================

        business_travel = st.selectbox(
            "Business Travel",
            [
                "Travel_Rarely",
                "Travel_Frequently",
                "Non-Travel"
            ]
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        overtime = st.selectbox(
            "OverTime",
            [
                "Yes",
                "No"
            ]
        )

    # ====================================
    # RIGHT COLUMN
    # ====================================

    with col2:

        department = st.selectbox(
            "Department",
            [
                "Sales",
                "Research & Development",
                "Human Resources"
            ]
        )

        education_field = st.selectbox(
            "Education Field",
            [
                "Life Sciences",
                "Medical",
                "Marketing",
                "Technical Degree"
            ]
        )

        job_role = st.selectbox(
            "Job Role",
            [
                "Sales Executive",
                "Research Scientist",
                "Manager",
                "Laboratory Technician"
            ]
        )

        marital_status = st.selectbox(
            "Marital Status",
            [
                "Single",
                "Married",
                "Divorced"
            ]
        )

        environment_satisfaction = st.slider(
            "Environment Satisfaction",
            1,
            5,
            3
        )

        job_satisfaction = st.slider(
            "Job Satisfaction",
            1,
            5,
            3
        )

        relationship_satisfaction = st.slider(
            "Relationship Satisfaction",
            1,
            5,
            3
        )

        work_life_balance = st.slider(
            "Work Life Balance",
            1,
            5,
            3
        )

    # ====================================
    # FINAL BUSINESS LOGIC SAFETY CLAMP
    # ====================================

    years_at_company = min(
        years_at_company,
        total_working_years
    )

    years_with_curr_manager = min(
        years_with_curr_manager,
        years_at_company
    )

    years_in_current_role = min(
        years_in_current_role,
        years_at_company
    )

    years_since_last_promotion = min(
        years_since_last_promotion,
        total_working_years
    )

    # ====================================
    # HR PROFILE SUMMARY
    # ====================================

    st.divider()

    st.info(

        f"""
        Employee Profile Summary

        • Age: {age}

        • Total Working Years: {total_working_years}

        • Years At Company: {years_at_company}

        • Years With Current Manager: {years_with_curr_manager}

        • Years In Current Role: {years_in_current_role}

        • Years Since Last Promotion: {years_since_last_promotion}
        """
    )

    # ====================================
    # RUN PREDICTION
    # ====================================

    if st.button(
        "Run Manual Prediction"
    ):

        employee_data = {

            "Age": age,

            "MonthlyIncome":
                monthly_income,

            "TotalWorkingYears":
                total_working_years,

            "DailyRate": 500,

            "YearsAtCompany":
                years_at_company,

            "YearsWithCurrManager":
                years_with_curr_manager,

            "BusinessTravel":
                business_travel,

            "Gender":
                gender,

            "OverTime":
                overtime,

            "DistanceFromHome": 5,

            "StockOptionLevel": 1,

            "NumCompaniesWorked": 2,

            "JobLevel": 2,

            "YearsInCurrentRole":
                years_in_current_role,

            "EnvironmentSatisfaction":
                environment_satisfaction,

            "JobSatisfaction":
                job_satisfaction,

            "JobInvolvement": 3,

            "TrainingTimesLastYear": 2,

            "YearsSinceLastPromotion":
                years_since_last_promotion,

            "RelationshipSatisfaction":
                relationship_satisfaction,

            "Department":
                department,

            "EducationField":
                education_field,

            "JobRole":
                job_role,

            "MaritalStatus":
                marital_status,

            "WorkLifeBalance":
                work_life_balance,

            # ====================================
            # STATIC IBM FIELDS
            # ====================================

            "Education": 3,

            "HourlyRate": 80,

            "MonthlyRate": 15000,

            "PercentSalaryHike": 15,

            "PerformanceRating": 3,

            "EmployeeCount": 1,

            "Over18": "Y",

            "StandardHours": 80
        }

        with st.spinner(
            "Predicting..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/predict/manual",

                    json=employee_data,

                    timeout=15
                )

                if response.status_code == 200:

                    result = response.json()

                    if result["success"]:

                        st.success(
                            "Prediction completed"
                        )

                        probability = result[
                            "attrition_probability"
                        ]

                        risk_level = result[
                            "risk_level"
                        ]

                        st.subheader(
                            "Prediction Result"
                        )

                        st.write(
                            f"Attrition Probability: {probability * 100:.2f}%"
                        )

                        if risk_level == "High":

                            st.error(
                                f"Risk Level: {risk_level}"
                            )

                            st.warning(
                                "Immediate retention action recommended"
                            )

                        elif risk_level == "Medium":

                            st.warning(
                                f"Risk Level: {risk_level}"
                            )

                            st.info(
                                "Monitor employee engagement closely"
                            )

                        else:

                            st.success(
                                f"Risk Level: {risk_level}"
                            )

                            st.info(
                                "Employee condition is stable"
                            )

                    else:

                        st.error(
                            result["error"]
                        )

                else:

                    st.error(
                        "Backend prediction failed"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to backend"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Request timeout"
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )