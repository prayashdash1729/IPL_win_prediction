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
        cities = ['Abu Dhabi - Sheikh Zayed Stadium',
                  'Ahmedabad - Sardar Patel Stadium, Motera',
                  'Bangalore - M Chinnaswamy Stadium',
                  'Chennai - MA Chidambaram Stadium, Chepauk',
                  'Cuttack - Barabati Stadium',
                  'Delhi - Arun Jaitley Cricket Stadium',
                  'Dharamsala',
                  'Dubai - Dubai International Cricket Stadium',
                  'Hyderabad',
                  'Indore - Holkar Cricket Stadium',
                  'Jaipur - Sawai Mansingh Stadium',
                  'Kolkata - Eden Gardens',
                  'Mohali - IS Bindra Stadium',
                  'Mumbai - Brabourne Stadium',
                  'Mumbai - Dr DY Patil Sports Academy',
                  'Mumbai - Wankhede Stadium',
                  'Pune - MCA Stadium',
                  'Pune - Maharashtra Cricket Association Stadium',
                  'Sharjah',
                  'Visakhapatnam - YSR Reddy Stadium']
        
        return cities
    

class pipe:
    def __init__(self):
        # Loading the models
        # self.pipe = pickle.load(open(r'models/model.pkl', 'rb'))
        self.ini1_pipe = pickle.load(open(r'models/ini1_rf.pkl', 'rb'))
        self.ini2_pipe = pickle.load(open(r'models/ini2_rf.pkl', 'rb'))
    
    # def predict_proba(self, input_df, ini):
    #     """
    #     Function to predict the probability of the input data
    #     params:
    #         input_df: DataFrame
    #             The input data
    #         ini: int
    #             The innings number
    #     return:
    #         The probability of the winning team being batting team
    #     """
    #     # return self.pipe.predict_proba(input_df)
    #     if ini == 1:
    #         return self.ini1_pipe.predict_proba(input_df)
    #     elif ini == 2:
    #         return self.ini2_pipe.predict_proba(input_df)

    
