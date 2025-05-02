import streamlit as st
import pandas as pd
import json
import matplotlib.gridspec as gridspec  # Add this import
import numpy as np

from user_details import input_user_details
from checkbox_change import on_change_checkbox
from save_selection import save_selections

from graph_most import plot_disc_graph_most
from graph_least import plot_disc_graph_least
from graph_change import plot_disc_graph_change

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tabulate import tabulate
import smtplib
import streamlit as st

import matplotlib.pyplot as plt

# Load mappings from JSON file
with open('disc_mappings.json', 'r') as f:
    mappings = json.load(f)

# Extract all mappings dynamically
all_mappings = [mappings[f"mapping{i}"] for i in range(1, 25)]  # Adjust range based on the number of mappings in your JSON

# Initialize session state to store user details and selections
if 'user_details' not in st.session_state:
    st.session_state.user_details = {
        "name": "",
        "date_of_birth": None,
        "gender": ""
    }

# Initialize session state to store selections
if 'most_likely' not in st.session_state:
    st.session_state.most_likely = [None] * len(all_mappings)

if 'least_likely' not in st.session_state:
    st.session_state.least_likely = [None] * len(all_mappings)

if 'disc_scores_most' not in st.session_state:
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'disc_scores_least' not in st.session_state:
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'current_section' not in st.session_state:
    st.session_state.current_section = 0  # Start at the first section

if 'same_option_error' not in st.session_state:
    st.session_state.same_option_error = False  # Initialize error flag

if 'user_selections' not in st.session_state:
    st.session_state.user_selections = []
    
if 'assessment_completed' not in st.session_state:
    st.session_state.assessment_completed = False  # Initialize assessment completion status

# Initialize the keys for checkboxes
st.session_state.checkbox_keys = [[[], []] for _ in all_mappings]  # Adjust lists based on the number of mappings

def plot_example_graph(ax):
    # Example data - using the exact values from the form's example
    labels = ['D', 'I', 'S', 'C']
    example_values = [2, 8, 2, 6]  # Match the example graph pattern
    
    # Plot setup
    positions = np.arange(len(labels))
    
    # Setup the grid
    ax.set_ylim(0, 21)
    ax.set_xlim(-0.5, len(labels) - 0.5)
    
    # Add major gridlines at specific intervals
    major_gridlines = [0, 4, 8, 12, 16, 20]
    for y in major_gridlines:
        ax.axhline(y=y, color='gray', linestyle='-', alpha=0.15, linewidth=0.8)
    
    # Add minor gridlines
    for y in range(21):
        if y not in major_gridlines:
            ax.axhline(y=y, color='gray', linestyle='-', alpha=0.1, linewidth=0.5)
    
    # Remove existing labels
    ax.set_yticklabels([])
    
    # Add number labels on left side - match exact font and position
    for i in range(21):
        if i in [0, 4, 8, 12, 16, 20]:  # Major numbers
            ax.text(-0.15, i, str(i), ha='right', va='center', fontsize=6, fontweight='medium')
    
    # Plot data points and lines - match exact style from example
    ax.plot(positions, example_values, 'ko-', linewidth=0.8, markersize=3.5, markerfacecolor='white')
    ax.plot(positions, example_values, 'ko', markersize=2, markerfacecolor='black')

    # Set up axis
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=8, fontweight='bold')
    
    # Title exactly as in form
    ax.set_title("Example:\nDISC", pad=5, fontsize=7, fontweight='bold')
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)

    return ax

def auto_mail_results(user_name):
    # Access secrets from the secrets.toml file
    me = st.secrets["email"]["me"]
    password = st.secrets["email"]["password"]
    you = st.secrets["email"]["you"]
    server = st.secrets["email"]["server"]

    # Prepare DISC data for the table in the new format
    text = f"""
    IMLDISCheights™ Personality System Graph Page

    Name: {user_name}                          Date: {st.session_state.user_details['date_of_birth'].strftime('%m/%d/%Y')}
    Organization: {st.session_state.user_details.get('organization', '')}
    Position: {st.session_state.user_details.get('position', '')}
    Email: {st.session_state.user_details.get('email')}
    Setting for Profile: {st.session_state.user_details['gender']}                Gender: {'☒' if st.session_state.user_details['gender'] == 'Male' else '☐'} Male  {'☐' if st.session_state.user_details['gender'] == 'Female' else '☐'} Female

    See Scoring Instructions on Page 3

                                D     I     S     C     ★     Total Score    Must Equal
    Row 1   First, enter the "MOST" scores in     {st.session_state.disc_scores_most['D']:2}     {st.session_state.disc_scores_most['I']:2}     {st.session_state.disc_scores_most['S']:2}     {st.session_state.disc_scores_most['C']:2}     {st.session_state.disc_scores_most['*']:2}     {sum(st.session_state.disc_scores_most.values()):9}        24
            Row 1 →
    
    Row 2   Next, enter the "LEAST" scores in    {st.session_state.disc_scores_least['D']:2}     {st.session_state.disc_scores_least['I']:2}     {st.session_state.disc_scores_least['S']:2}     {st.session_state.disc_scores_least['C']:2}     {st.session_state.disc_scores_least['*']:2}     {sum(st.session_state.disc_scores_least.values()):9}        24
            Row 2 →
    
    Row 3   Then, subtract Row 2 from Row 1 →   {(st.session_state.disc_scores_most['D'] - st.session_state.disc_scores_least['D']):3}     {(st.session_state.disc_scores_most['I'] - st.session_state.disc_scores_least['I']):3}     {(st.session_state.disc_scores_most['S'] - st.session_state.disc_scores_least['S']):3}     {(st.session_state.disc_scores_most['C'] - st.session_state.disc_scores_least['C']):3}            Do not calculate ★ value for Row 3

    NOTE: If the Row 2 ("LEAST") number is larger than the Row 1 ("MOST") number, the number will be negative ("-") in Row 3.
    REMEMBER: The "+" and "-" numbers can ONLY be plotted on GRAPH 3.

    Graphing:
    A. Plot Row 1 "MOST" onto Graph 1.
    B. Plot Row 2 "LEAST" onto Graph 2.
    C. Plot Row 3 "CHANGE" onto Graph 3. (Watch positive and negative numbers!)
    D. Connect the D - I - S - C dots on each of the three graphs. See Example below
    """

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.4; }}
            .header {{ text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
            .profile-info {{ margin: 10px 0; }}
            .profile-info table {{ width: 100%; }}
            .profile-info td {{ padding: 2px; }}
            .scoring-table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            .scoring-table th, .scoring-table td {{ border: 1px solid black; padding: 5px; text-align: center; }}
            .scoring-table th {{ font-weight: bold; background-color: #ddd; }}
            .row-header {{ text-align: left; font-weight: bold; background-color: #ddd; }}
            .instructions {{ text-align: left; font-style: italic; }}
            .note {{ margin: 10px 0; font-style: italic; }}
            .graphing {{ margin: 10px 0; }}
            .graphing ol {{ margin-left: 20px; }}
            .graphs {{ margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">IMLDISCheights™ Personality System Graph Page</div>
        
        <div class="profile-info">
            <table>
                <tr>
                    <td><strong>Name:</strong> {user_name}</td>
                    <td><strong>Date:</strong> {st.session_state.user_details['date_of_birth'].strftime('%m/%d/%Y')}</td>
                </tr>
                <tr>
                    <td><strong>Organization:</strong> {st.session_state.user_details.get('organization', '')}</td>
                    <td><strong>Email:</strong> {st.session_state.user_details.get('email', '')}</td>
                </tr>
                <tr>
                    <td><strong>Position:</strong> {st.session_state.user_details.get('position', '')}</td>
                    <td><strong>Gender:</strong> {'☒' if st.session_state.user_details['gender'] == 'Male' else '☐'} Male  {'☐' if st.session_state.user_details['gender'] == 'Female' else '☐'} Female</td>
                </tr>
            </table>
        </div>

        <p><strong>See Scoring Instructions on Page 3</strong></p>

        <table class="scoring-table">
            <tr>
                <th colspan="2"></th>
                <th style="background-color: #ddd;">D</th>
                <th style="background-color: #ddd;">I</th>
                <th style="background-color: #ddd;">S</th>
                <th style="background-color: #ddd;">C</th>
                <th style="background-color: #ddd;">★</th>
                <th style="background-color: #ddd;">Total</th>
                <th style="background-color: #ddd;">Must Equal</th>
            </tr>
            <tr>
                <td class="row-header">Row 1<br>Most</td>
                <td class="instructions">First, enter the "MOST" scores in Row 1 →</td>
                <td>{st.session_state.disc_scores_most['D']}</td>
                <td>{st.session_state.disc_scores_most['I']}</td>
                <td>{st.session_state.disc_scores_most['S']}</td>
                <td>{st.session_state.disc_scores_most['C']}</td>
                <td>{st.session_state.disc_scores_most['*']}</td>
                <td>{sum(st.session_state.disc_scores_most.values())}</td>
                <td>24</td>
            </tr>
            <tr>
                <td class="row-header">Row 2<br>Least</td>
                <td class="instructions">Next, enter the "LEAST" scores in Row 2 →</td>
                <td>{st.session_state.disc_scores_least['D']}</td>
                <td>{st.session_state.disc_scores_least['I']}</td>
                <td>{st.session_state.disc_scores_least['S']}</td>
                <td>{st.session_state.disc_scores_least['C']}</td>
                <td>{st.session_state.disc_scores_least['*']}</td>
                <td>{sum(st.session_state.disc_scores_least.values())}</td>
                <td>24</td>
            </tr>
            <tr>
                <td class="row-header">Row 3<br>Change</td>
                <td class="instructions">Then, subtract Row 2 from Row 1 →</td>
                <td>{st.session_state.disc_scores_most['D'] - st.session_state.disc_scores_least['D']}</td>
                <td>{st.session_state.disc_scores_most['I'] - st.session_state.disc_scores_least['I']}</td>
                <td>{st.session_state.disc_scores_most['S'] - st.session_state.disc_scores_least['S']}</td>
                <td>{st.session_state.disc_scores_most['C'] - st.session_state.disc_scores_least['C']}</td>
                <td colspan="3">Do not calculate ★ value for Row 3</td>
            </tr>
        </table>

        <div class="note">
            <p><strong>NOTE:</strong> If the Row 2 ("LEAST") number is larger than the Row 1 ("MOST") number, the number will be negative ("-") in Row 3.</p>
            <p><strong>REMEMBER:</strong> The "+" and "-" numbers can ONLY be plotted on GRAPH 3.</p>
        </div>

        <div class="graphing">
            <p><strong>Graphing:</strong></p>
            <ol type="A">
                <li>Plot Row 1 "MOST" onto Graph 1.</li>
                <li>Plot Row 2 "LEAST" onto Graph 2.</li>
                <li>Plot Row 3 "CHANGE" onto Graph 3. (Watch positive and negative numbers!)</li>
                <li>Connect the D - I - S - C dots on each of the three graphs. See Example below</li>
            </ol>
        </div>

        <div class="graphs">
            <img src="cid:image1" style="width: 100%; margin-top: 20px;">
        </div>
        
        <div class="note">
            <p><strong>Note:</strong> If you cannot find the exact number for your score on a graph, estimate between the two closest numbers on any given line.</p>
        </div>
    </body>
    </html>
    """

    # Construct the email
    message = MIMEMultipart("related")
    message['Subject'] = f"DISC Assessment Results | {user_name}"
    message['From'] = me
    message['To'] = you

    # Attach text and HTML versions of the email
    message_alternative = MIMEMultipart("alternative")
    message.attach(message_alternative)
    message_alternative.attach(MIMEText(text, 'plain'))
    message_alternative.attach(MIMEText(html, 'html'))
    
    # Create a figure with specific dimensions to match the form
    fig = plt.figure(figsize=(10, 2.8))  # Reduced height from 3 to 2.8
    
    # Create a grid of subplots without the example graph
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1], wspace=0.4)  # Increased wspace from 0.3 to 0.4
    
    # Create the three main graph axes (without example graph)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    
    # Plot the data
    values_most = [st.session_state.disc_scores_most[cat] for cat in ['D', 'I', 'S', 'C']]
    values_least = [st.session_state.disc_scores_least[cat] for cat in ['D', 'I', 'S', 'C']]
    values_change = [m - l for m, l in zip(values_most, values_least)]

    plot_disc_graph_most(values_most, ax1)
    plot_disc_graph_least(values_least, ax2)
    plot_disc_graph_change(values_change, ax3)
    
    # Fine-tune the layout
    plt.subplots_adjust(
        top=0.85,      # Reduced from original
        bottom=0.2,    # Increased from original
        left=0.1,
        right=0.95,
        wspace=0.4     # Added explicit wspace here too
    )
    
    # Save with adjusted padding
    fig.savefig('/tmp/all_disc_graphs.png', 
        dpi=300, 
        bbox_inches='tight',
        pad_inches=0.1  # Reduced padding
    )
    
    # Attach the combined image to the email
    file_path = '/tmp/all_disc_graphs.png'
    with open(file_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<image1>')
        message.attach(img)

    # Send the email
    smtp_server = smtplib.SMTP(server)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(me, password)
    smtp_server.sendmail(me, you, message.as_string())
    smtp_server.quit()
    print('Email sent successfully')
    

# Calculate DISC scores after saving selections
def calculate_disc_scores():
    # Initialize DISC scores
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

    # Loop through saved selections to calculate DISC scores
    for selection in st.session_state.user_selections:
        idx = selection["section"]
        most_option = selection["most_likely"]
        least_option = selection["least_likely"]

        most_disc_type = all_mappings[idx][most_option]["most"]
        least_disc_type = all_mappings[idx][least_option]["least"]

        st.session_state.disc_scores_most[most_disc_type] += 1  # Increment for Most Likely
        st.session_state.disc_scores_least[least_disc_type] += 1  # Increment for Least Likely

# Show the form or the result depending on the assessment completion status
if st.session_state.current_section == 0:
    input_user_details()  # First, prompt the user to fill in their details
elif not st.session_state.assessment_completed:
    idx = st.session_state.current_section - 1  # Adjust the section index because the first section is user details
    mapping = all_mappings[idx]

# Calculate progress
    progress = f"{idx + 1}/{len(all_mappings)}"

    # Create the table layout with checkboxes
    st.write(f"### DISC Personality Assessment ({progress})")
    st.write("""Choose the option which best reflects your personality. Select one option as the **most likely** and one option as the **least likely**.""")
    st.write("""This form should be completed within **7 minutes**, or as close to that as possible.""")

    col1, col2, col3 = st.columns([1, 1, 5])

    with col1:
        st.write("**Most Likely**")
        for option in mapping.keys():
            key = f"most_{idx}_{option}"
            st.checkbox("", key=key, on_change=on_change_checkbox, args=(key, idx, 0))
            st.session_state.checkbox_keys[idx][0].append(key)

    with col2:
        st.write("**Least Likely**")
        for option in mapping.keys():
            key = f"least_{idx}_{option}"
            st.checkbox("", key=key, on_change=on_change_checkbox, args=(key, idx, 1))
            st.session_state.checkbox_keys[idx][1].append(key)

    with col3:
        st.write("**Options**")
        for option in mapping.keys():
            st.write(option)

    # Display the same option error message
    if st.session_state.same_option_error:
        st.error("You cannot select the same option for both 'Most Likely' and 'Least Likely'. Please choose different options.")

    # Validation and Submission
    most_likely_selected = any(st.session_state.get(key) for key in st.session_state.checkbox_keys[idx][0])
    least_likely_selected = any(st.session_state.get(key) for key in st.session_state.checkbox_keys[idx][1])

    if most_likely_selected and least_likely_selected:
        if idx < len(all_mappings) - 1:
            # Handle button click before rerendering the UI
            if st.button("Next"):
                save_selections(idx)
                st.session_state.current_section += 1
                st.rerun()  # Force a rerun to immediately update the section
        else:
            if st.button("Submit"):
                save_selections(idx)
                # Reset DISC scores before calculation
                calculate_disc_scores()
                st.session_state.assessment_completed = True
                st.rerun()  # Force a rerun to display the result
    else: 
        st.error("Please make a selection for both 'Most Likely' and 'Least Likely' options.")
# ...

else:
    # Calculate the sum for each row
    sum_most = sum(st.session_state.disc_scores_most.values())
    sum_least = sum(st.session_state.disc_scores_least.values())

    # Calculate the difference between Most Likely and Least Likely (excluding the * column)
    diff_D = st.session_state.disc_scores_most["D"] - st.session_state.disc_scores_least["D"]
    diff_I = st.session_state.disc_scores_most["I"] - st.session_state.disc_scores_least["I"]
    diff_S = st.session_state.disc_scores_most["S"] - st.session_state.disc_scores_least["S"]
    diff_C = st.session_state.disc_scores_most["C"] - st.session_state.disc_scores_least["C"]
    diff_total = diff_D + diff_I + diff_S + diff_C

    # Prepare data for the table including the sum and difference row
    data = {
        "Category": ["Most Likely", "Least Likely", "Difference"],
        "D": [st.session_state.disc_scores_most["D"], st.session_state.disc_scores_least["D"], diff_D],
        "I": [st.session_state.disc_scores_most["I"], st.session_state.disc_scores_least["I"], diff_I],
        "S": [st.session_state.disc_scores_most["S"], st.session_state.disc_scores_least["S"], diff_S],
        "C": [st.session_state.disc_scores_most["C"], st.session_state.disc_scores_least["C"], diff_C],
        "*": [st.session_state.disc_scores_most["*"], st.session_state.disc_scores_least["*"], "-"],  # Exclude * from Difference calculation
        "Total": [sum_most, sum_least, diff_total]  # Add the sum as the final column
    }

    df = pd.DataFrame(data)
        
    # Plot the line graphs
    categories = ["D", "I", "S", "C"]
    most_likely_scores = [st.session_state.disc_scores_most[cat] for cat in categories]
    least_likely_scores = [st.session_state.disc_scores_least[cat] for cat in categories]
    difference_scores = [diff_D, diff_I, diff_S, diff_C]
    
    # Thank you message
    user_name = st.session_state.user_details['name']
    auto_mail_results(user_name)
    st.success(f"Thank you, {user_name}, for completing the assessment! Your results have been sent to Dino.")

