import streamlit as st 


# st.write("Hello, Respond 2!")
# welcome
st.write(f'Xin chào **{st.session_state["user"]}**')
st.write(f'Chức danh: *{st.session_state['role']}*')