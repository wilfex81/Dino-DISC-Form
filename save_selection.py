import streamlit as st

# Function to save user's selections for the current section
def save_selections(idx):
    most_likely_key = next((key for key in st.session_state.checkbox_keys[idx][0] if st.session_state.get(key)), None)
    least_likely_key = next((key for key in st.session_state.checkbox_keys[idx][1] if st.session_state.get(key)), None)

    if most_likely_key and least_likely_key:
        most_option = most_likely_key.split("_")[2]
        least_option = least_likely_key.split("_")[2]

        # Save the selection as a dictionary
        st.session_state.user_selections.append({
            "section": idx,
            "most_likely": most_option,
            "least_likely": least_option
        })
        
