import streamlit as st
import streamlit_authenticator as stauth
import datetime
import yagmail

import pandas as pd 
import numpy as np
from glob import glob
import os
import time
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# import dthu
# import cphi
# import tkho
# import kqkd
# import kh

from helper import *

# https://api.github.com/repos/Huynh-Tr/report/contents/

# layout wide
st.set_page_config(layout='wide')
# hide menu
st.markdown(
    """
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > header > div.stAppToolbar.st-emotion-cache-15ecox0.e4hpqof2 {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# center of the layout
st.markdown('<h1 style="text-align: center;">Chi Tiết Chi Phí</h1>', unsafe_allow_html=True)
st.divider()

st.header('Welcome to the dash board page!')
st.subheader(f'Today: {datetime.datetime.now().strftime('%d-%m-%Y')}')


st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

if "otp" not in st.session_state:
    st.session_state.otp = None  # Start with no OTP

if "otp_generated" not in st.session_state:
    st.session_state.otp_generated = False # start with no OTP generated

if not st.session_state.otp_generated: # Only generate if OTP is not generated yet.
    OTP = np.random.randint(1000, 9999)
    # np.random.seed(0) # Keep seed for testing purpose. Remove it in production.
    st.session_state.otp = OTP  # Store OTP in session state
    # st.write(OTP)

send_to_email = st.text_input('fill out the email')
if st.button("Send Email") and not st.session_state.otp_generated:  # Only send if OTP hasn't been sent.
    try:
        yag = yagmail.SMTP(st.secrets["gmail"]["user"], st.secrets["gmail"]["password"])
        yag.send(
            to=[send_to_email, st.secrets["gmail"]["user"]],
            subject="OTP Test!",
            contents=f'{st.session_state.otp}'  # Use the stored OTP
        )
        st.success("Email sent successfully!")
        st.session_state.otp_generated = True # Mark as generated
    except Exception as e:
        st.error(f"Error sending email: {e}")

# st.session_state

# OTP_check = st.text_input('OTP', 0)

if st.session_state.otp is not None and int(OTP_check) == st.session_state.otp:
    st.write('Right')
elif st.session_state.otp is not None and int(OTP_check)!= st.session_state.otp and OTP_check!= '0': # Added this condition to avoid showing "wrong" immediately.
    st.write('Wrong')

def clearss():
    st.session_state.otp = None
    st.session_state.otp_generated = False

if st.button('clear session state'):
    clearss()
    st.write('Session state cleared!')
    # st.session_state

# authentication
usernames = ['admin', 'user']
# password = ['admin', 'user']
# credentials = {'usernames': {'jsmith': {'email': 'jsmith@gmail.com', 'failed_login_attempts': 0, 'first_name': 'John', \
#       'last_name': 'Smith', 'logged_in': False, 'password': '12345'}, 
#                             'rbriggs': {'email': 'abc@gmail.com', 'failed_login_attempts': 0, 'first_name': 'Robert', \
#       'last_name': 'Briggs', 'logged_in': False, 'password': '1234'}
#                             }
#                 }

_x = ['a', 'b', 'c']
_y = ['huynh.th@pnj.com.vn', 'loan.ttt01@pnj.com.vn', 'huynhvietjetair@gmail.com']
_z = ['g', 'h', 'i']
_a = ['g', 'h', 'i']

# c2 = {'username': {'roles': {'name':'email': 'a', 'password': 'b'}}}

n = [{'name': a, 'email': y, 'password': z} for a, y, z in zip(_a, _y, _z)]
credentials = {'usernames': {x: i for x, i in zip(_x, n)}}
st.write(credentials)
# }

# emails = ['admin', 'user']
# roles = ['admin', 'user']
# OTP = ['123456', '123456']

authenticator = stauth.Authenticate(credentials=credentials)
# authenticator = stauth.Authenticate(usernames, password)
# try:
authenticator.login()
# except LoginError as e:
#     st.error(e)
if st.session_state.authentication_status:
    st.write("User is authenticated")

# st.session_state

if st.session_state["authentication_status"]:
    # st.write('___')
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    # st.title('Some content')    
    # st.write('___')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# st.session_state

# st.session_state.authentication_status == False

# df = cphi.cphi()

# st.write(df)