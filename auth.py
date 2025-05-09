import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def get_auth():
    try:
        if not os.path.exists('auth_config.yaml'):
            return create_default_config()
            
        with open('auth_config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
            
            # Validate the config structure
            if not all(key in config for key in ['credentials', 'cookie']):
                st.warning("Invalid config structure, creating default...")
                return create_default_config()
                
            return stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config.get('allow_signup', False)
            )
            
    except Exception as e:
        st.error(f"Auth error: {str(e)}")
        return create_default_config()

def create_default_config():
    """Initialize with default admin credentials"""
    default_config = {
        'cookie': {
            'expiry_days': 30,
            'key': 'your-unique-secret-key-123',  # Change this!
            'name': 'ckd_app_cookie'
        },
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@example.com',
                    'name': 'Admin',
                    'password': stauth.Hasher(['admin123']).generate()[0]
                }
            }
        },
        'preauthorized': {'emails': []}
    }
    
    # Save the default config
    with open('auth_config.yaml', 'w') as file:
        yaml.dump(default_config, file)
        
    return stauth.Authenticate(
        default_config['credentials'],
        default_config['cookie']['name'],
        default_config['cookie']['key'],
        default_config['cookie']['expiry_days']
    )