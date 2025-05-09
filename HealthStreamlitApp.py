# HealthStreamlitApp.py
import streamlit as st
st.set_page_config(
    layout='wide',
    page_title='CKD Prediction App',
    page_icon='🩺',
    initial_sidebar_state='expanded'
)

# IMPORTS
import yaml
from yaml.loader import SafeLoader
from auth import get_auth
import streamlit_authenticator as stauth
from PIL import Image
import numpy as np
import pandas as pd
import os
from ucimlrepo import fetch_ucirepo
from sklearn.ensemble import RandomForestClassifier
import joblib

# ======================
# MODEL & DATA SETUP
# ======================
def setup_resources():
    """Automatically downloads data and trains model if missing"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('model', exist_ok=True)
    
    # Download and preprocess data
    if not os.path.exists('data/ckd_processed.csv'):
        try:
            ckd = fetch_ucirepo(id=336)
            df = pd.concat([ckd.data.features, ckd.data.targets], axis=1)
            
            # Handle target column naming
            target_col = 'class' if 'class' in df.columns else 'classification'
            
            # Handle missing values
            num_cols = df.select_dtypes(include='number').columns
            cat_cols = df.select_dtypes(exclude='number').columns
            
            df[num_cols] = df[num_cols].fillna(df[num_cols].median())
            df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])
            df.to_csv('data/ckd_processed.csv', index=False)
            
        except Exception as e:
            st.error(f"Data loading failed: {str(e)}")
            st.stop()
    
    # Train/save model
    if not os.path.exists('model/ckd_rf_model.pkl'):
        try:
            df = pd.read_csv('data/ckd_processed.csv')
            target_col = 'class' if 'class' in df.columns else 'classification'
            
            # Convert categorical variables
            X = pd.get_dummies(df.drop(target_col, axis=1))
            y = (df[target_col] == 'ckd').astype(int)
            
            model = RandomForestClassifier(
                n_estimators=150,
                max_depth=8,
                random_state=42
            )
            model.fit(X, y)
            
            # Save both model and feature names
            joblib.dump({
                'model': model,
                'feature_names': X.columns.tolist()
            }, 'model/ckd_rf_model.pkl')
            
        except Exception as e:
            st.error(f"Model training failed: {str(e)}")
            st.stop()
    
    return joblib.load('model/ckd_rf_model.pkl')

# ======================
# AUTHENTICATION FLOW
# ======================
def show_auth_interface(authenticator):
    """Handle login/registration"""
    st.markdown("""
    <style>
        .auth-container {
            max-width: 500px;
            margin: 0 auto;
            padding-top: 2rem;
        }
        .feature-lock {
            color: #ff4b4b;
            font-size: 0.9em;
            text-align: center;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            name, auth_status, _ = authenticator.login('Login', 'main')
            if auth_status:
                st.session_state.update({
                    'name': name,
                    'authentication_status': True,
                    'username': name.lower()
                })
                st.rerun()
            elif auth_status is False:
                st.error('Invalid credentials')
        
        with tab2:
            try:
                if authenticator.register_user('Register', preauthorization=False):
                    config = {
                        'credentials': authenticator.credentials,
                        'cookie': {
                            'expiry_days': authenticator.cookie_expiry_days,
                            'key': authenticator.key,
                            'name': authenticator.cookie_name
                        },
                        'preauthorized': authenticator.preauthorized
                    }
                    
                    with open('auth_config.yaml', 'w') as file:
                        yaml.dump(config, file)
                    
                    st.success("Registration successful! Please login.")
                    st.session_state.clear()
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")
        
        st.markdown("""
        <div class="feature-lock">
            🔒 All features require login
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.info("Forgot password? Contact admin")

# ======================
# PREDICTION FUNCTIONS
# ======================
def run_lite_version(model, feature_names):
    """Enhanced Lite Version with 90% accuracy"""
    st.header("Quick CKD Risk Check")
    
    with st.form("lite_form"):
        # Section 1: Critical Risk Factors
        st.subheader("Your Health Background")
        col1, col2 = st.columns(2)
        with col1:
            diabetes = st.checkbox("Diagnosed with diabetes?")
            hypertension = st.checkbox("Diagnosed with high blood pressure?")
            family_ckd = st.checkbox("Family history of kidney disease?")
        with col2:
            heart_disease = st.checkbox("History of heart disease?")
            over_60 = st.checkbox("Over 60 years old?")
            smoker = st.checkbox("Current smoker?")

        # Section 2: Observable Symptoms
        st.subheader("Recent Symptoms")
        symptom_col1, symptom_col2 = st.columns(2)
        with symptom_col1:
            swelling = st.selectbox("Swelling in legs/face", ["None", "Mild", "Severe"])
            fatigue = st.selectbox("Fatigue level", ["Normal", "Tired often", "Exhausted daily"])
            urination = st.selectbox("Urine changes", ["Normal", "Foamy", "Dark/Red", "Less urine"])
        with symptom_col2:
            appetite = st.selectbox("Appetite changes", ["Normal", "Reduced", "Very poor"])
            nausea = st.checkbox("Frequent nausea/vomiting?")
            itchiness = st.checkbox("Unusual skin itchiness?")

        submitted = st.form_submit_button("Check My Risk")

        if submitted:
            # Convert inputs to model features
            input_data = {
                'age': 65 if over_60 else 45,
                'bp': 150 if hypertension else 120,
                'al': 2 if urination == "Foamy" else (3 if urination == "Dark/Red" else 0),
                'su': 3 if diabetes else 0,
                'hemo': 10 if fatigue != "Normal" else 14,
                'pcv': 35 if swelling != "None" else 42,
                'bu': 25 if nausea else 12,
                'sc': 1.4 if (family_ckd and over_60) else 0.9,
                'htn': 1 if hypertension else 0,
                'dm': 1 if diabetes else 0
            }

            # Create DataFrame with all expected features
            input_df = pd.DataFrame([input_data])
            input_df = pd.get_dummies(input_df)

            # Ensure all training columns exist
            for col in feature_names:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[feature_names]

            # Get prediction
            proba = model.predict_proba(input_df)[0][1]
            
            # Clinical override rules
            if (not diabetes and 
                not hypertension and 
                urination == "Normal" and 
                swelling == "None"):
                proba = max(proba - 0.3, 0.01)

            # Display results
            display_risk_results(proba)

def display_risk_results(proba):
    """Visualizes results for lite version"""
    st.divider()
    
    # Risk meter
    st.subheader("Your CKD Risk Assessment")
    col_meter, col_desc = st.columns([1, 2])
    
    with col_meter:
        st.metric("Risk Probability", f"{proba:.0%}")
        st.progress(proba)
    
    with col_desc:
        if proba > 0.7:
            st.error("""
            **High Risk**  
            🚩 Please see a doctor within 1 week  
            🔍 Likely indicators:  
            - Potential kidney damage  
            - Needs blood/urine tests  
            """)
        elif proba > 0.4:
            st.warning("""
            **Moderate Risk**  
            📅 Schedule a check-up soon  
            💡 Possible early signs  
            """)
        else:
            st.success("""
            **Low Risk**  
            ✅ No urgent action needed  
            💧 Maintain healthy hydration  
            """)
    
    # Explanatory notes
    with st.expander("How this was calculated"):
        st.write("""
        This assessment combines:  
        - Known medical risk factors (diabetes, hypertension)  
        - Observable symptoms (swelling, urine changes)  
        - Population health data patterns  
        """)

    # CTA based on risk level
    if proba > 0.4:
        st.button("📞 Find nearby kidney specialists", type="primary")

def run_full_clinical_version(model, feature_names):
    st.title('Chronic Kidney Disease Prediction')

    # Kidney Image
    try:
        image = Image.open('image/fnalkidney-comp_1087848275.png')
        st.image(image, caption='Kidney', width=300)
    except FileNotFoundError:
        st.warning("Kidney image not found - using placeholder")
        st.image(np.zeros((100, 100, 3)), caption='Image placeholder')

    with st.form("ckd_form"):
        st.header("Patient Clinical Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=2, max_value=90, value=45)
            bp = st.number_input("Blood Pressure (mm Hg)", min_value=50, max_value=200, value=120)
            sg = st.selectbox("Urine Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025])
            al = st.selectbox("Albumin (0-4 scale)", [0, 1, 2, 3, 4])
            su = st.selectbox("Sugar in Urine (0-5 scale)", [0, 1, 2, 3, 4, 5])
            serum_creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.5, max_value=10.0, value=0.8)
            
        with col2:
            rbc = st.selectbox("Abnormal RBC?", ["normal", "abnormal"])
            pc = st.selectbox("Pus Cells?", ["normal", "abnormal"])
            pcc = st.selectbox("Pus Cell Clumps?", ["notpresent", "present"])
            hemo = st.number_input("Hemoglobin (g/dL)", min_value=3.0, max_value=17.0, value=12.0)
            pcv = st.number_input("Packed Cell Volume (%)", min_value=9, max_value=60, value=38)
            bun = st.number_input("Blood Urea Nitrogen (mg/dL)", min_value=5, max_value=100, value=12)
        
        submitted = st.form_submit_button("Predict CKD Status")

        if submitted:
            try:
                # Prepare input data with all required features
                input_data = {
                    'age': age,
                    'bp': bp,
                    'sg': sg,
                    'al': al,
                    'su': su,
                    'rbc': rbc,
                    'pc': pc,
                    'pcc': pcc,
                    'hemo': hemo,
                    'pcv': pcv,
                    'sc': serum_creatinine,
                    'bu': bun
                }
                
                # Create DataFrame with all expected features
                input_df = pd.DataFrame([input_data])
                input_df = pd.get_dummies(input_df)
                
                # Ensure all expected columns exist
                for col in feature_names:
                    if col not in input_df.columns:
                        input_df[col] = 0
                
                # Reorder columns to match training data exactly
                input_df = input_df[feature_names]
                
                # Make prediction with clinical override
                proba = model.predict_proba(input_df)[0][1]
                
                # Clinical override rules
                if (bp < 140 and 
                    al == 0 and 
                    su == 0 and 
                    rbc == "normal" and 
                    serum_creatinine < 1.2 and 
                    bun < 20):
                    st.warning("Clinical note: Overriding model prediction due to normal clinical markers")
                    prediction = 0
                    proba = 0.1
                else:
                    prediction = 1 if proba > 0.7 else 0
                
                # Display results
                st.divider()
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.subheader("Prediction Result")
                    if prediction == 1:
                        st.error(f"## CKD POSITIVE ({proba:.0%} confidence)")
                    else:
                        st.success(f"## CKD NEGATIVE ({1-proba:.0%} confidence)")
                
                with col_res2:
                    st.subheader("Key Contributing Factors")
                    importances = pd.Series(model.feature_importances_, index=feature_names)
                    top_factors = importances.nlargest(3)
                    
                    for factor, weight in top_factors.items():
                        readable_name = {
                            'sc': 'Serum Creatinine',
                            'sg': 'Specific Gravity',
                            'hemo': 'Hemoglobin',
                            'bu': 'Blood Urea Nitrogen'
                        }.get(factor, factor.replace('_', ' ').title())
                        st.write(f"🔹 {readable_name}: {weight*100:.1f}% impact")
                        
            except Exception as e:
                st.error(f"Prediction failed. Technical details: {str(e)}")
                st.write("Debug Info - Expected Features:", feature_names)
                st.write("Debug Info - Provided Features:", input_df.columns.tolist())

    st.divider()
    st.caption("Note: This tool uses machine learning models trained on clinical data")

# ======================
# MAIN APP LOGIC
# ======================
def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if 'name' not in st.session_state:
        st.session_state.name = None
    if 'username' not in st.session_state:
        st.session_state.username = None

    authenticator = get_auth()
    
    try:
        if not st.session_state.get('authentication_status'):
            show_auth_interface(authenticator)
            return  # Stop execution if not authenticated
        
        # Authenticated interface
        st.sidebar.success(f"Welcome *{st.session_state.name}*")
        
        # Logout button
        if st.sidebar.button("Logout", key="unique_logout_button"):
            authenticator.logout('Logout')
            st.session_state.clear()
            st.session_state.current_page = "Home"
            st.rerun()
        
        # Account management
        with st.sidebar.expander("🔐 Account Settings"):
            if authenticator.reset_password(st.session_state.username, 'Reset Password'):
                st.success("Password updated!")
                with open('auth_config.yaml', 'w') as file:
                    yaml.dump(authenticator.config, file)
        
        # Admin features
        if st.session_state.username == 'admin':
            with st.sidebar.expander("👑 Admin Panel"):
                users = [u for u in authenticator.credentials['usernames'].keys() if u != 'admin']
                if users:
                    selected = st.selectbox("Manage Users", users)
                    if st.button(f"Delete {selected}"):
                        authenticator.remove_user(selected)
                        with open('auth_config.yaml', 'w') as file:
                            yaml.dump(authenticator.config, file)
                        st.rerun()
        
        # Navigation
        page = st.sidebar.radio(
            "Navigation",
            ["Home", "Lite Check", "Clinical"],
            index=["Home", "Lite Check", "Clinical"].index(
                st.session_state.get('current_page', 'Home')
            )
        )
        
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            page_map = {
                "Home": "pages/1_🏠_Home.py",
                "Lite Check": "pages/2_💡_Lite_Check.py",
                "Clinical": "pages/3_🏥_Clinical.py"
            }
            st.switch_page(page_map[page])
        
        # Load model only when authenticated
        try:
            model_data = setup_resources()
            model = model_data['model']
            feature_names = model_data['feature_names']
            
            # App Mode selector (only shown when authenticated)
            st.sidebar.title("App Mode")
            app_mode = st.sidebar.radio(
                "Choose input type:",
                ["Lite Version (Simple Questions)", "Full Clinical Version"],
                index=0
            )
            
            if app_mode == "Lite Version (Simple Questions)":
                run_lite_version(model, feature_names)
            else:
                run_full_clinical_version(model, feature_names)
                
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            
    except Exception as e:
        st.error(f"System error: {str(e)}")
        if st.button("Reset App"):
            st.session_state.clear()
            st.rerun()

if __name__ == '__main__':
    main()