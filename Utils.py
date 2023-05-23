import base64
import streamlit as st
import pickle


# Getting the image as base64 since direct paths is not working
@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

class Image:
    def get_bg_img(self, file):
        return get_img_as_base64(file)
    
    def get_sidebar_img(self, file):
        return get_img_as_base64(file)

class PageStyle:
    def page_style(self, bg_img, sidebar_img):
        # Setting the page style and making the bg image responsive
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
            [data-testid="stHorizontalBlock"]{{
                background-color: #fff;
                background-color: rgba(255,255,255,0.5);
                border-radius: 1.0rem;
                padding: 1.0rem;
            }}
        </style>
        """
        return page_style
    
class IPL:
    def get_teams(self):
        teams = ['Chennai Super Kings',
            'Delhi Capitals',
            'Kings XI Punjab',
            'Kolkata Knight Riders',
            'Mumbai Indians',
            'Rajasthan Royals',
            'Royal Challengers Bangalore',
            'Sunrisers Hyderabad']
        
        return teams
    
    def get_venues(self):
        cities = ['Bengaluru', 'Mohali', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Ahmedabad', 'Cuttack', 'Nagpur',
       'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi',
       'Abu Dhabi', 'Sharjah', 'Dubai', 'Indore']
        
        return cities
    

class pipe:
    def __init__(self):
        # Loading the model
        self.pipe = pickle.load(open('./model.pkl', 'rb'))
    
    def predict_proba(self, input_df):
        return self.pipe.predict(input_df)

    