import streamlit as st
import sqlite3
st.set_page_config('Disease Detection', '🍪', layout='wide',menu_items=None,initial_sidebar_state='collapsed')
   

if "authType" not in st.session_state:
    st.session_state.authType = 'Login'


@st.dialog("Authentication")
def login():
    if st.session_state.authType == 'Login':


        st.write(f"Please Log In To Continue With This App?")
        st.text_input("username",key="username")
        if st.session_state.username:
            st.text_input("password",key="password",type='password')

        col1, col2 = st.columns(2,gap='small',border=True,vertical_alignment='center')
        with col1:
            if st.button("Submit"):
                st.session_state.userID =1
                st.session_state.auth_timer=100000
                st.switch_page(page="pages/diabetes.py")
                st.rerun()
                return ""
        with col2:
            if st.button("Register",type='primary'):
                st.session_state.authType = 'Register'
                st.rerun()



    elif st.session_state.authType == 'Register':
        st.write(f"Please Register In To Continue With This App?")
        st.text_input("username",key="username")
        st.text_input("Password",key="Password")
        if st.session_state.username:
            st.text_input("password",key="password",type='password')
        col1, col2 = st.columns(2,gap='small',border=True,vertical_alignment='center')
        with col1:
            if st.button("Submit"):
                
                st.rerun()
                return ""
        with col2:
            if st.button("Login",type='primary'):
                st.session_state.authType = 'Login'
                st.rerun()

if "userID" not in st.session_state:
    st.session_state.userID = login()


if "auth_timer" not in st.session_state:
    st.session_state.auth_timer = 1

@st.fragment(run_every=st.session_state.auth_timer)
def check_if_user_logged_in():
    try:    
        if type(st.session_state.userID) != type(1):
            login()
        else:
            pass       
    except :
        pass



check_if_user_logged_in()

