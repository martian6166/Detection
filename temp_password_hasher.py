# Generate hashes like this (run once in a temp file)
import streamlit_authenticator as stauth
hashed_pw = stauth.Hasher(['your_password']).generate()
print(hashed_pw)