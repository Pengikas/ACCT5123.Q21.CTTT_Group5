# Import thư viện Streamlit để tạo giao diện web
import streamlit as st
# Import requests để gọi API backend
import requests

st.set_page_config(
    page_title="Employee Attrition Predictor",
    layout="centered"
)

# TITLE
# Hiển thị tiêu đề hệ thống
st.title("Employee Attrition Prediction System")
# Header
st.header("Employee Information")

# INPUT FORM
# Number input cho tuổi
age = st.number_input(
    "Age",
    min_value=18,
    max_value=65,
    value=30
)

# Number input cho salary
salary = st.number_input(
    "Salary",
    min_value=1000,
    value=5000
)

# Dropdown chọn job role
job_role = st.selectbox(
    "Job Role",
    ["Manager", "Sales Executive", "Research Scientist"]
)

# Number input số năm làm việc
years_at_company = st.number_input(
    "Years at Company",
    min_value=0,
    max_value=40,
    value=5
)

# Slider mức độ hài lòng công việc
job_satisfaction = st.slider(
    "Job Satisfaction",
    1,
    4,
    3
)

# Dropdown overtime
overtime = st.selectbox(
    "Overtime",
    ["Yes", "No"]
)

# Divider
st.divider()

# PREDICT BUTTON
if st.button("Predict"):

    # Validation
    if age <= 0:
        st.error("Age must be greater than 0")

    elif salary <= 0:
        st.error("Salary must be greater than 0")

    else:

        # JSON data
        data = {
            "age": age,
            "salary": salary,
            "job_role": job_role,
            "years_at_company": years_at_company,
            "job_satisfaction": job_satisfaction,
            "overtime": overtime
        }

        # Loading spinner
        with st.spinner("Predicting..."):

            try:

                # API request
                response = requests.post(
                    "http://127.0.0.1:5000/predict",
                    json=data,
                    timeout=10
                )

                # Status check
                if response.status_code == 200:

                    result = response.json()

                    st.success("Prediction completed successfully")

                    # Get results
                    probability = result["attrition_probability"]

                    risk_level = result["risk_level"]

                    # DISPLAY RESULT
                    st.subheader("Prediction Result")

                    st.write(
                        f"Attrition Probability: {probability*100:.2f}%"
                    )

                    # Risk display
                    if risk_level == "High":

                        st.error(f"Risk Level: {risk_level}")

                    elif risk_level == "Medium":

                        st.warning(f"Risk Level: {risk_level}")

                    else:

                        st.success(f"Risk Level: {risk_level}")

                    # Recommendation
                    st.subheader("Recommendation")

                    if risk_level == "High":

                        st.write(
                            "Take retention action immediately"
                        )

                    elif risk_level == "Medium":

                        st.write(
                            "Monitor employee condition"
                        )

                    else:

                        st.write(
                            "Employee condition is stable"
                        )

                else:

                    st.error("Backend returned an error")

            except requests.exceptions.ConnectionError:

                st.error("Cannot connect to backend")

            except requests.exceptions.Timeout:

                st.error("Request timeout")

            except Exception as e:

                st.error(f"Unexpected error: {e}")