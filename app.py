import streamlit as st
import pandas as pd
import pickle
import numpy as np
import Utils as utils
import fetch_live_data



# Making ojects
Img = utils.Image()
PageStyle = utils.PageStyle()
IPL = utils.IPL()
pipe = utils.pipe()

# Setting background and sidebar images
bg_img = Img.get_bg_img('./images/pattern1.png')
sidebar_img = Img.get_sidebar_img('./images/pattern5.png')

# Setting up the page style
page_style = PageStyle.page_style(bg_img, sidebar_img)

st.markdown(page_style, unsafe_allow_html=True)


# Building the dashboard
st.title('IPL win prediction')
st.sidebar.title('Welcome to IPL Win Predictor')
st.sidebar.header('Select your choice')
# Adding options to the sidebar
sidebar = st.sidebar.selectbox('Live Match or Custom Match?', ('Live Match', 'Custom Match'))

if (sidebar == 'Live Match'):
    # Getting the live matches
    st.subheader("Today's Matches-")
    
    try:
        Data = fetch_live_data.Data()
        matches_id, code = Data.get_matches()
    except:
        st.write("For local hosting, override the default API to local file. If not running locally, Check API request limit.")
        # break out of the loop
        st.stop()
 
    if code == 200:

        if(len(matches_id) == 0):
            st.subheader("_No matches today!_")
            
        else:
            # match 0 is the first match of the day
            col1, col2 = st.columns(2)
            with st.container():
                # Getting the match details
                match = Data.get_match_details(matches_id[0])

                if(match['live_details'] == None):
                    col1.write('This match has not started yet')
                    with col2:
                        st.subheader(match["fixture"]["home"]['name'] + ' vs ' + match["fixture"]["away"]['name'])
                        st.write("Venue: " + match["fixture"]['venue'])

                elif (match['live_details']["match_summary"]["in_play"] == "No"):
                    live = match["live_details"]["match_summary"]
                    col1.subheader(live["status"])
                    with col2:
                        st.write(live["toss"])
                        if(len(live["away_scores"]) > len(live["home_scores"])):
                            st.write("Scores: " + live["away_scores"])
                        else:
                            st.write("Scores: " + live["home_scores"])
                        st.write("Venue: " + match["fixture"]['venue'])

                elif (len(match["live_details"]["scorecard"]) == 1):
                    live = match["live_details"]["scorecard"][0]
                    col1.subheader(match["fixture"]["home"]['name'] + ' vs ' + match["fixture"]["away"]['name'])
                    col1.write('Wait for 2nd inning to show win probability')
                    with col2:
                        st.write("Batting team: " + live["title"].replace("Innings", ""))
                        st.write("Score: " + str(live["runs"]) + "/" + live["wickets"])
                        st.write("Overs: " + live["overs"])
                        st.write("Venue: " + match["fixture"]['venue'])

                else:
                    live = match["live_details"]

                    try:
                        batting_team = match["live_details"]["scorecard"][1]["title"].replace(" Innings", "")
                        bowling_team = match["live_details"]["scorecard"][0]["title"].replace(" Innings", "")
                        venue = match["fixture"]['venue'].split(",")[-1].split(" ")[1]
                        target = match["live_details"]["scorecard"][0]["runs"]
                        crr = float(match["live_details"]["stats"]["current_run_rate"])
                        runs = match["live_details"]["scorecard"][1]["runs"]
                        wickets_fallen = int(match["live_details"]["scorecard"][1]["wickets"])
                        wickets_left = 10 - wickets_fallen
                        overs = float(match["live_details"]["scorecard"][1]["overs"].split(".")[0])
                        runs_to_bat = target - runs
                        balls_left = 120 - (int(overs) * 6 + (overs % 1) * 10)
                        rrr = runs_to_bat / (balls_left / 6)

                        with col2:
                            st.write("Batting team: " + batting_team)
                            st.write("Score: " + str(runs) + "/" + str(wickets_fallen))
                            st.write("Overs: " + str(overs))
                            st.write("Target: " + str(target))
                            st.write("Venue: " + match["fixture"]['venue'])

                        input_df = pd.DataFrame({
                            'batting_team': [batting_team],
                            'bowling_team': [bowling_team],
                            'venue': [venue],
                            'runs_to_bat': [runs_to_bat],
                            'balls_left': [balls_left],
                            'wickets_left': [wickets_left],
                            'target': [target],
                            'crr': [crr],
                            'rrr': [rrr]
                        })

                        try:
                            result = pipe.predict_proba(input_df)

                            loss = result[0][0]
                            win = result[0][1]
                            # Printing the predicted probabilities
                            col1.header(batting_team + "- " + str(round(win*100)) + "%")
                            col1.header(bowling_team + "- " + str(round(loss*100)) + "%")

                        except:
                            col1.write("_There seems to be some error. Please try again later._")

                    except:
                        col1.subheader(match['live_details']["match_summary"]["status"])
                        with col2:
                            st.subheader(match["fixture"]["home"]['name'] + ' vs ' + match["fixture"]["away"]['name'])
                            st.write("Venue: " + match["fixture"]['venue'])
                            

            # match 1 is the second match of the day
            if(len(matches_id)==2):
                col3, col4 = st.columns(2)
                with st.container():
                    # Getting the match details
                    match = Data.get_match_details(matches_id[1])

                    if(match['live_details'] == None):
                        col1.write('This match has not started yet')
                        with col2:
                            st.subheader(match["fixture"]["home"]['name'] + ' vs ' + match["fixture"]["away"]['name'])
                            st.write("Venue: " + match["fixture"]['venue'])

                    elif (match['live_details']["match_summary"]["in_play"] == "No"):
                        live = match["live_details"]["match_summary"]
                        col1.subheader(live["status"])
                        with col2:
                            st.write(live["toss"])
                            if(len(live["away_scores"]) > len(live["home_scores"])):
                                st.write("Scores: " + live["away_scores"])
                            else:
                                st.write("Scores: " + live["home_scores"])
                            st.write("Venue: " + match["fixture"]['venue'])

                    elif (len(match["live_details"]["scorecard"]) == 1):
                        live = match["live_details"]["scorecard"][0]
                        col1.subheader(match["fixture"]["home"]['name'] + ' vs ' + match["fixture"]["away"]['name'])
                        col1.write('Wait for 2nd inning to show win probability')
                        with col2:
                            st.write("Batting team: " + live["title"].replace("Innings", ""))
                            st.write("Score: " + str(live["runs"]) + "/" + live["wickets"])
                            st.write("Overs: " + live["overs"])
                            st.write("Venue: " + match["fixture"]['venue'])

                    else:
                        live = match["live_details"]

                        batting_team = live["title"].replace(" Innings", "")
                        bowling_team = match["live_details"]["scorecard"][0]["title"].replace(" Innings", "")
                        venue = match["fixture"]['venue'].split(",")[-1].split(" ")[1]
                        target = match["live_details"]["scorecard"][0]["runs"]
                        crr = int(match["live_details"]["stats"]["current_run_rate"])
                        runs = match["live_details"]["scorecard"][1]["runs"]
                        wickets_fallen = match["live_details"]["scorecard"][1]["wickets"]
                        wickets_left = 10 - wickets_fallen
                        overs = match["live_details"]["scorecard"][1]["overs"].split(".")[0]
                        runs_to_bat = target - runs
                        balls_left = 120 - (overs.split(".")[0] * 6 + overs.split(".")[1])
                        rrr = runs_to_bat / (balls_left / 6)

                        with col2:
                            st.write("Batting team: " + batting_team)
                            st.write("Score: " + str(runs) + "/" + str(wickets_fallen))
                            st.write("Overs: " + overs)
                            st.write("Target: " + str(target))
                            st.write("Venue: " + match["fixture"]['venue'])

                        input_df = pd.DataFrame({
                            'batting_team': [batting_team],
                            'bowling_team': [bowling_team],
                            'venue': [venue],
                            'runs_to_bat': [runs_to_bat],
                            'balls_left': [balls_left],
                            'wickets_left': [wickets_left],
                            'target': [target],
                            'crr': [crr],
                            'rrr': [rrr]
                        })

                        try:
                            result = pipe.predict_proba(input_df)

                            loss = result[0][0]
                            win = result[0][1]
                            # Printing the predicted probabilities
                            col1.header(batting_team + "- " + str(round(win*100)) + "%")
                            col1.header(bowling_team + "- " + str(round(loss*100)) + "%")

                        except:
                            col1.write("_There seems to be some error. Please try again later._")
    
    elif code == 429:
        st.write("Status Code 429: API limit reached. Please try again later.")
    
    else:
        st.write("API error. Status Code " + str(code) + ": Something went wrong. Please try again later.")


elif (sidebar == 'Custom Match'):

    st.subheader('Welcome to Custom Match')
    teams = IPL.get_teams()
    stadiums = IPL.get_venues()
    

    col1, col2 = st.columns(2)
    batting_team = ''
    bowling_team = ''
    # getting the user input through input boxes.
    with col1:
        batting_team = st.selectbox('Select the Batting team', sorted([x for x in teams if x != bowling_team]))
    with col2:
        bowling_team = st.selectbox('Select the Bowling team', sorted([x for x in teams if x != batting_team]))

    col3 = st.columns(1)[0]
    with col3:
        match_stadium = st.selectbox('Select venue', sorted(stadiums))

    col4, col5 = st.columns(2)
    with col4:
        innings = st.selectbox('Select the Innings', ('1st Innings', '2nd Innings'))
    with col5:
        target = st.number_input('Target (for 2nd Innings)', value=1, min_value=1, step=1)

    col6, col7, col8 = st.columns(3)
    with col6:
        score = st.number_input('Current Score', min_value=0, step=1)
    with col7:
        overs = st.number_input('Current Over', value=0., min_value=0., max_value=20., step=0.1)
        disable_predict = (overs - int(overs) > 0.5)
        if(disable_predict):
            st.error('Invalid Over details. Please enter a valid over')
    with col8:
        wickets = st.number_input('Wickets down', min_value=0, max_value=10)

    if st.button('Predict Win Probability', help='Predict!', disabled=disable_predict):
        data_valid = True
        runs_to_bat = target - score
        # balls_left = 120 - (int(overs)*6 + round((overs - int(overs)))*10)
        balls_left = 120 - int(overs*6)
        wickets_left = 10 - wickets
        if(overs == 0):
            data_valid = False
            crr = 0
            st.error('0 Overs bowled. Please enter valid over details.')
        else:
            crr = score/(int(overs)*6 + round((overs - int(overs)))*10)
        rrr = runs_to_bat/(balls_left/6)

        # Features required for the model
        # ['batting_team', 'bowling_team', 'city', 'runs_to_bat', 'balls_left', 'wickets_left', 'target', 'crr', 'rrr']
        # making a dataframe from the inputs

        input_df_ini2 = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city_stadium': [match_stadium],
            'runs_to_bat': [runs_to_bat],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'rrr': [rrr]
        })

        input_df_ini1 = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city_stadium': [match_stadium],
            'runs': [score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
        })

        if(data_valid):
            if(innings == '1st Innings'):
                result = pipe.ini1_pipe.predict_proba(input_df_ini1)
            else:
                result = pipe.ini2_pipe.predict_proba(input_df_ini2)

            loss = result[0][0]
            win = result[0][1]
            # Printing the predicted probabilities
            st.header(batting_team + "- " + str(round(win*100)) + "%")
            st.header(bowling_team + "- " + str(round(loss*100)) + "%")

        # except:
        #     st.write("_Something went wrong :(. Try refreshing the page._")

        

        





    

    

