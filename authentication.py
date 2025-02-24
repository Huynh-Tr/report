import streamlit as st 
import pandas as pd 
import time

# layout wide
# st.set_page_config(layout='wide')
# hide menu
# st.markdown(
#     """
#     <style>
#     #root > div:nth-child(1) > div.withScreencast > div > header > div.stAppToolbar.st-emotion-cache-15ecox0.e4hpqof2 {
#         visibility: hidden;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # starttime
# start = time.time()


# st.html('''
# <style>
# div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
#     max-height: 38px !important; /* Fix the height */
#     overflow: auto !important;
# }
# </style>
# ''')

p = r'D:\pnj.com.vn\HuynhTN - Documents\Project\streamlit\dims\dsql.xlsx'
df = pd.read_excel(p)
df['user'] = df['Email'].str.split('@').str[0]
df['pwd'] = [str(i) for i in range(len(df))]
# df

# roles = df['Chức danh'].unique()

# tab1, tab2 = st.tabs(['login', 'register'])

# login

st.session_state.role = None

def login():
    name = st.text_input('Username', key='name')
    password = st.text_input('Password', type='password', key='password')
    if st.button('Login'):
        # st.session_state
        if (password == df[df['user']==name]['pwd'].values):
            st.session_state.role = role
            st.session_state.user = df[df['user']==name]['HỌ VÀ TÊN'].values[0]
            st.session_state.role = df[df['user']==name]['Chức danh'].values[0]
            st.session_state.email = df[df['user']==name]['Email'].values[0]
            st.write(f'Xin chào **{st.session_state["user"]}**')
            st.write(f'Chức danh: *{st.session_state['role']}*')
            st.rerun()

def logout():
    # st.button('Logout', on_click=st.session_state.clear)
    # st.session_state.authentication_status = False
    st.session_state.role = None
    st.rerun()

#         # elif st.session_state["authentication_status"] is False:
#         #     st.error('Username/password is incorrect')
#         # elif st.session_state["authentication_status"] is None:
#         #     st.warning('Please enter your username and password')

# # login()
# # logout()

# # reg
# name_reg = tab2.text_input('New Username', key='name_reg')
# password_reg = tab2.text_input('New Password', type='password', key='password_reg')

# if tab2.button('Register'):
#     if name_reg in credentials:
#         tab2.error('Username already exists')
#     else:
#         credentials[name_reg] = {'name': name_reg, 'pwd': password_reg}
#         tab2.success('User registered successfully')
# credentials

import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester", "Responder", "Admin"]


def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon="✔")
settings = st.Page("settings.py", title="Settings", icon="⚙️")
request_1 = st.Page(
    "pages/Chi Tiết Chi Phí.py",
    title="Request 1",
    icon="✌",
    default=(role == "Quản lý - Marketing"),
)
request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon="✌"
)
respond_1 = st.Page(
    "pages/Dashboard.py",
    title="Respond 1",
    icon="✌",
    default=(role == "Quản lý nhóm - Hành chính"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon="✌"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon="✌",
    default=(role == "Giám đốc - Chi nhánh"),
)
admin_2 = st.Page("pages/Giá Vàng.py", title="Admin 2", icon="✌")

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Request manager")
# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.role in ["Giám đốc - Chi nhánh", "Quản lý nhóm - Hành chính"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Giám đốc - Chi nhánh", "Quản lý - Marketing"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Giám đốc - Chi nhánh":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()

st.session_state