import streamlit as st

# Define a function to ensure only one checkbox is selected at a time in a column
def on_change_checkbox(current_key, idx, column):
    # Ensure only one checkbox is selected in the current column
    for key in st.session_state.checkbox_keys[idx][column]:
        if key != current_key:
            st.session_state[key] = False

    # Check if the same option is selected for both most and least likely
    other_column = 1 - column
    current_option = current_key.split("_")[2]
    conflicting_key = f"{'most' if other_column == 0 else 'least'}_{idx}_{current_option}"
    
    if st.session_state.get(current_key) and st.session_state.get(conflicting_key):
        st.session_state[current_key] = False  # Reset the current selection
        st.session_state.same_option_error = True  # Set error flag
    else:
        st.session_state.same_option_error = False  # Reset error flag if no conflict
