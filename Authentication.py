import streamlit as st 
import pandas as pd 
import time
import dim

# layout wide
st.set_page_config(layout='wide')

# add logo
st.logo(size="medium", link="https://cdn.pnj.io/images/logo/pnj.com.vn.png")
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

# https://api.github.com/repos/Huynh-Tr/report/contents/

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

df = dim.dsql()

if "level" not in st.session_state:
    st.session_state.level = None

col1, col2, col3 = st.columns([1, 1, 1])

def login():
    col2.header("Log in")
    # role = st.selectbox("Choose your role", ROLES)
    name = col2.text_input('Username', key='name')
    password = col2.text_input('Password', type='password', key='password')

    if col2.button("Log in"):
        if (password == df[df['user']==name]['pwd'].values):
            # st.session_state.role = role
            st.session_state.user = df[df['user']==name]['HỌ VÀ TÊN'].values[0]
            st.session_state.role = df[df['user']==name]['Chức danh'].values[0]
            st.session_state.email = df[df['user']==name]['Email'].values[0]
            st.session_state.level = df[df['user']==name]['Cấp'].values[0]
            st.session_state.Aut = df[df['user']==name]['Aut'].values[0]
            # st.write(f'Xin chào **{st.session_state["user"]}**')
            # st.write(f'Chức danh: *{st.session_state['role']}*')
            st.rerun()
        # st.session_state.role = role
        # st.rerun()


def logout():
    # st.session_state.user = None
    # st.session_state.level = None
    # st.session_state.role = None
    st.session_state.clear()
    st.rerun()

level = st.session_state.level

logout_page = st.Page(logout, title="Log out", icon="✔")
settings = st.Page("Chatbot.py", title="AI-ChatBot", icon="🧠")
request_1 = st.Page(
    "Cửa Hàng/Chi Tiết Chi Phí.py",
    title="Cửa Hàng 1",
    icon="✌",
    default=(level == 0),
)
request_2 = st.Page(
    "Cửa Hàng/Cửa Hàng 2.py", title="Cửa Hàng 2", icon="✌"
)
respond_1 = st.Page(
    "Phòng Ban/Dashboard.py",
    title="Phòng Ban 1",
    icon="✌",
    default=(level == 1),
)
respond_2 = st.Page(
    "Phòng Ban/Phòng Ban 2.py", title="Phòng Ban 2", icon="✌"
)
admin_1 = st.Page(
    "Quản Lý/Report PnL.py",
    title="Quản Lý 1",
    icon="✌",
    default=(level == 3),
)
admin_2 = st.Page("Quản Lý/Giá Vàng.py", title="Quản Lý 2", icon="✌")

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.level in [0, 3]:
    page_dict["Cửa Hàng"] = request_pages
if st.session_state.level in [1, 3]:
    page_dict["Phòng Ban"] = respond_pages
if st.session_state.level in [3]:
    page_dict["Quản Lý"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()

# st.session_state
