login_url = 'https://disease-detection-i6n9.onrender.com/auth/login'

signup_url= 'https://disease-detection-i6n9.onrender.com/auth/signup'


import requests
import json

def login_func(url,username, password):
    # Headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Payload with user data
    data = {
     
        "username": username,
        "password": password
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        return response.json()  # Return the response as a JSON
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        print("Response:", response.text)
        return None



def signUp_func(url, firstName, lastName, username, password):
    # Headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Payload with user data
    data = {
        "firstName": firstName,
        "lastName": lastName,
        "username": username,
        "password": password
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        return response.json()  # Return the response as a JSON
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        print("Response:", response.text)
        return None



import streamlit as st
st.set_page_config('Disease Detection', '🍪', layout='wide',menu_items=None,initial_sidebar_state='expanded')
   

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
                st.session_state.userID  = login_func(login_url,st.session_state.username,st.session_state.password)
                if st.session_state.userID:
                    st.session_state.auth_timer=100000
                    st.switch_page(page="pages/diabetes.py")
                    st.rerun()
                    return ""
                else:
                    st.error("Incorrect Login Details Entered")
        with col2:
            if st.button("Register",type='primary'):
                st.session_state.authType = 'Register'
                st.rerun()



    elif st.session_state.authType == 'Register':
        st.write(f"Please Register In To Continue With This App?")
        st.text_input("first Name",key="fistName")
        st.text_input("last Name",key="lastName")
        st.text_input("username",key="username")
        if st.session_state.username:
            st.text_input("password",key="password",type='password')
        col1, col2 = st.columns(2,gap='small',border=True,vertical_alignment='center')
        with col1:
            if st.button("Submit"):
                st.session_state.userID = signUp_func(signup_url,st.session_state.firstName,st.session_state.lastName,st.session_state.username,st.session_state.password)
                if st.session_state.userID:
                    st.session_state.auth_timer=100000
                    st.switch_page(page="pages/diabetes.py")
                    st.rerun()
                    return ""
                else:
                    st.error("Incorrect Login Details Entered")
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
