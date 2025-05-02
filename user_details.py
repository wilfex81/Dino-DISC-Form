import streamlit as st
from datetime import date, datetime

# Function to handle the first section for user details
def input_user_details():
    st.write(f"### DISC Personality Assessment")
    st.write("""Your Payment has been processed! For any queries, please contact dinogrif@gmail.com""")
    st.write("### Please fill in your details")
    
    # Get name with validation (required)
    name = st.text_input("Name*", value=st.session_state.user_details.get("name", ""))
    
    # Get date of birth (optional)
    dob = st.date_input("Date of Birth", value=st.session_state.user_details.get("date_of_birth"))
    
    # Get gender (optional)
    gender = st.selectbox("Gender", ["", "Male", "Female"], index=0 if not st.session_state.user_details.get("gender") else 
                         ["", "Male", "Female"].index(st.session_state.user_details["gender"]))
    
    # Get email with validation (required)
    email = st.text_input("Email*", value=st.session_state.user_details.get("email", ""))
    
    # Validate email format
    def is_valid_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    # Show continue button only if required fields are filled
    if name and email:
        if not is_valid_email(email):
            st.error("Please enter a valid email address")
        elif not name.strip():
            st.error("Please enter your name")
        else:
            if st.button("Continue"):
                # Save user details
                st.session_state.user_details = {
                    "name": name,
                    "date_of_birth": dob if dob else None,
                    "gender": gender if gender else "",
                    "email": email
                }
                st.session_state.current_section = 1
                st.rerun()
    else:
        st.warning("Please fill in all required fields marked with *")
