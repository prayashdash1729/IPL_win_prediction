import streamlit as st
import pandas as pd
import pickle
import numpy as np
# import requests
import base64

@st.cache_data

def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = get_img_as_base64('./images/pattern1.png')
sidebar_img = get_img_as_base64('./images/pattern5.png')

page_style = f"""
<style>
    .sidebar .sidebar-content {{
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }}
    [data-testid="stMarkdownContainer"] {{
        font-weight: bold;
    }}
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{bg_img}");
        background-size: cover;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        # background-attachment: local;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background-image: url("data:image/png;base64,{sidebar_img}");
        background-size: cover;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        # background-attachment: local;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)


st.title('IPL win prediction')
st.sidebar.title('Welcome to IPL Win Predictor')
st.sidebar.header('Select your choice')
sidebar = st.sidebar.selectbox('Live Match or Custom Match?', ('Live Match', 'Custom Match'))

if (sidebar == 'Live Match'):
    st.subheader('Ongoing Match-')
    st.markdown("   ***Live match feature will be added shortly...***")

elif (sidebar == 'Custom Match'):
    st.subheader('Welcome to Custom Match')

    teams = ['Chennai Super Kings',
             'Delhi Capitals',
             'Kings XI Punjab',
             'Kolkata Knight Riders',
             'Mumbai Indians',
             'Rajasthan Royals',
             'Royal Challengers Bangalore',
             'Sunrisers Hyderabad']
    
    stadiums = ['Arun Jaitley Cricket Stadium',
                'Barabati Stadium',
                'Brabourne Stadium',
                'Buffalo Park',
                'De Beers Diamond Oval',
                'Dr DY Patil Sports Academy',
                'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
                'Dubai International Cricket Stadium',
                'Eden Gardens',
                'Himachal Pradesh Cricket Association Stadium',
                'Holkar Cricket Stadium',
                'JSCA International Stadium Complex',
                'Kingsmead',
                'M Chinnaswamy Stadium',
                'MA Chidambaram Stadium, Chepauk',
                'Maharashtra Cricket Association Stadium',
                'New Wanderers Stadium',
                'Newlands',
                'OUTsurance Oval',
                'Punjab Cricket Association Stadium, Mohali',
                'Rajiv Gandhi International Stadium, Uppal',
                'Sardar Patel Stadium, Motera',
                'Sawai Mansingh Stadium',
                'Shaheed Veer Narayan Singh International Stadium',
                'Sharjah Cricket Stadium',
                'Sheikh Zayed Stadium',
                "St George's Park",
                'SuperSport Park',
                'Vidarbha Cricket Association Stadium, Jamtha',
                'Wankhede Stadium']
    
    pipe = pickle.load(open('./model.pkl', 'rb'))

    col1, col2 = st.columns(2)
    batting_team = ''
    bowling_team = ''
    with col1:
        batting_team = st.selectbox('Select the Batting team', sorted([x for x in teams if x != bowling_team]))
    with col2:
        bowling_team = st.selectbox('Select the Bowling team', sorted([x for x in teams if x != batting_team]))

    match_stadium = st.selectbox('Select host Stadium',sorted(stadiums))

    target = st.number_input('Target', value=0, min_value=0, step=1)

    col3, col4, col5 = st.columns(3)
    with col3:
        score = st.number_input('Current Score', min_value=0, step=1)
    with col4:
        overs = st.number_input('Current Over', value=0, min_value=0, max_value=20, step=1)
    with col5:
        wickets = st.number_input('Wickets down', min_value=0, max_value=10)

    if st.button('Predict Win Probability', help='Predict!'):
        runs_to_bat = target - score
        # balls_left = 120 - (int(overs)*6 + round((overs - int(overs)))*10)
        balls_left = 120 - int(overs*6)
        wickets_left = 10 - wickets
        crr = score/(int(overs)*6 + round((overs - int(overs)))*10)
        rrr = runs_to_bat/(balls_left/6)

# ['batting_team', 'bowling_team', 'venue', 'runs_to_bat', 'balls_left', 'wickets_left', 'target', 'crr', 'rrr']

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'venue': [match_stadium],
            'runs_to_bat': [runs_to_bat],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'target': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)

        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + "- " + str(round(win*100)) + "%")
        st.header(bowling_team + "- " + str(round(loss*100)) + "%")
        

        





    

    

