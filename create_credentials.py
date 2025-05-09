# create_credentials.py
import streamlit_authenticator as stauth
import yaml

# Generate hashed password for "admin123"
hashed_passwords = stauth.Hasher(['admin123']).generate()

# Basic auth config
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'email': 'admin@example.com',
                'name': 'Admin',
                'password': hashed_passwords[0]
            }
        }
    },
    'cookie': {
        'name': 'ckd_app_cookie',
        'key': 'your-random-key-here',  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
        'expiry_days': 30
    },
    'preauthorized': {
        'emails': ['admin@example.com']
    }
}

# Save to auth_config.yaml
with open('auth_config.yaml', 'w') as file:
    yaml.dump(config, file)

print("Created auth_config.yaml with default admin credentials:")
print("Username: admin")
print("Password: admin123")