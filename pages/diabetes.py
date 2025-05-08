import streamlit as st
from auth import get_auth
import pandas as pd
import joblib

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.warning("Please login from main app")
    st.stop()


import time
import streamlit as st
from tensorflow.keras.models import load_model # type: ignore
import numpy as np
import pandas as pd
# Example input (should have the same 21 features as training data)

st.set_page_config(page_title="Diabetes Prediction",page_icon="🍧")

st.title("Fill in the form to make a prediction")
if "userID" not in st.session_state:
    st.session_state.userID = None  
        
if "auth_timer" not in st.session_state:
    st.session_state.auth_timer = 1



if st.session_state.userID ==None:
    st.switch_page("main.py")
def get_selectbox_indices():
    # Define the options for each selectbox
    label_dict = {
        "HighBP": "Do you have High Blood Pressure ",
        "HighChol": "Do you have High Cholestral ",
        "Cholcheck": "Have you gone to get your cholestral check within the last 5 days",
        "Smoker": "Have you smoked up to 100 cigarettes",
        "Stroke": "Ever had a stroke",
        "HeartDiseaseorAttack": "Do you have History of heart disease or heart attack in your family ",
        "PhysActivity": "Have you participated in a Physical activity in the last 30 days",
        "Fruits": "Do you Eats fruits at least once per day",
        "Veggies": "Do you Eats Veggies at least once per day",
        "HvyAlcoholConsump": "Are you a heavy consumer of alchol",
        "AnyHealthcare": "Do you have a health care plan",
        "NoDocbcCost": "Are you unable to see a doctor due to cost",
        "DiffWalk": "Do you have difficult walking",
        "Sex": "Whats your sex",
        "Age": "Whats your age group",
        "Education": "Whats your highest Education Level",
        "Income":"What's your Monthly income level"
    }
    options_dict = {
        "HighBP": ["No", "Yes"],
        "HighChol": ["No", "Yes"],
        "Cholcheck": ["No", "Yes"],
        "Smoker": ["No", "Yes"],
        "Stroke": ["No", "Yes"],
        "HeartDiseaseorAttack": ["No", "Yes"],
        "PhysActivity": ["No", "Yes"],
        "Fruits": ["Yes", "No"],
        "Veggies": ["Yes", "No"],
        "HvyAlcoholConsump": ["No", "Yes"],
        "AnyHealthcare": ["No", "Yes"],
        "NoDocbcCost": ["No", "Yes"],
        "DiffWalk": ["No", "Yes"],
        "Sex": ["Male", "Female"],
        "Age": ["18-24", "25-29", "30-35", "36-40", "41-45", "46-50", "50-60", "60+"],
        "Education": ["No schooling", "Middle School/Primary School", "Technical/Vocational School", "High School",
                      "College graduate", "Masters Graduate/Doctorate", "PHD Graduate"],
        "Income": ["<₦10k", "₦10k-₦20k", "₦21k-₦40k", "₦41k-₦60k", "₦61k-₦65k", "₦66k-₦69k", "₦70k-₦75k", "₦75k+"]
    }
    
    # Get the indices of selected options
    selected_indices = {}
    
    for key, options in options_dict.items():
        selected_value = st.selectbox(
            label=label_dict[key],
            options=options,
            key=key
        )
        # Get the index of the selected value
        selected_index = options.index(selected_value)
        selected_indices[key] = selected_index
        
    # Return the dictionary of selected indices
    return selected_indices

# Call the function to get selected indices

st.number_input(label="How much do you weigh",min_value=10,step=1,max_value=1000,key="weight")
st.number_input(label="How tall are you in feet",step=1,min_value=1,max_value=14,key="height")

st.select_slider(
    label="Rate How Unhealthy you feel on a scale of 1 through 10 and 1 is for very healthy and physically fit 10 is for not really healthy or physically fit",
    options=[1,2,3,4,5,6,7,8,9,10],
    key="GenHlth"
)

st.number_input(
    label="Number of days mental health was not good in the last 30 days ",
   step=1,
   max_value=30,
   min_value=0,
    key="MentHlth"
)
st.number_input(
    label="Number of days physical health was not good in the last 30 days",
   step=1,
   max_value=30,
   min_value=0,
    key="PhysHlth"
)
if "new_data" not in st.session_state:
    st.session_state.new_data=np.array([[  
    0,    # HighBP (No)
    0,    # HighChol (No)
    1,    # CholCheck (Yes)
    22,   # BMI (Healthy range: 18.5-24.9)
    0,    # Smoker (No)
    0,    # Stroke (No)
    0,    # HeartDiseaseorAttack (No)
    1,    # PhysActivity (Yes, Active)
    1,    # Fruits (Eats daily)
    1,    # Veggies (Eats daily)
    0,    # HvyAlcoholConsump (No heavy drinking)
    1,    # AnyHealthcare (Has healthcare)
    0,    # NoDocbcCost (No financial issues)
    1,    # GenHlth (Excellent health, scale: 1-5)
    0,    # MentHlth (No bad mental health days in last 30 days)
    0,    # PhysHlth (No bad physical health days in last 30 days)
    0,    # DiffWalk (No difficulty walking)
    1,    # Sex (Male)
    3,    # Age (25-29 age group)
    5,    # Education (College Graduate)
    7     # Income ($75k-$100k)
]])





def compute_bmi(weight, height):
    """
    Compute BMI from weight and height.
    Assumes weight is in kilograms and height is in feet.
    Converts height to meters (1 foot = 0.3048 meters) and rounds BMI to the nearest integer.
    """
    height_m = height * 0.3048
    bmi = weight / (height_m ** 2)
    return int(round(bmi))

def create_feature_list(indices):
    """
    Create a list of features in the desired order:
      0: HighBP (selectbox)
      1: HighChol (selectbox)
      2: Cholcheck (selectbox)
      3: BMI (computed from weight and height)
      4: Smoker (selectbox)
      5: Stroke (selectbox)
      6: HeartDiseaseorAttack (selectbox)
      7: PhysActivity (selectbox)
      8: Fruits (selectbox)
      9: Veggies (selectbox)
     10: HvyAlcoholConsump (selectbox)
     11: AnyHealthcare (selectbox)
     12: NoDocbcCost (selectbox)
     13: GenHlth (select_slider; assumed available directly from st.session_state)
     14: MentHlth (number_input)
     15: PhysHlth (number_input)
     16: DiffWalk (selectbox)
     17: Sex (selectbox)
     18: Age (selectbox)
     19: Education (selectbox)
     20: Income (selectbox)
    """
    # Compute BMI using the number inputs from session_state
    bmi = compute_bmi(st.session_state["weight"], st.session_state["height"])
    
    feature_list = [
        indices['HighBP'],             # HighBP (No/Yes)
        indices['HighChol'],           # HighChol (No/Yes)
        indices['Cholcheck'],          # Cholcheck (No/Yes)
        bmi,                           # BMI (computed)
        indices['Smoker'],             # Smoker (No/Yes)
        indices['Stroke'],             # Stroke (No/Yes)
        indices['HeartDiseaseorAttack'],  # HeartDiseaseorAttack (No/Yes)
        indices['PhysActivity'],       # PhysActivity (No/Yes)
        indices['Fruits'],             # Fruits (No/Yes)
        indices['Veggies'],            # Veggies (No/Yes)
        indices['HvyAlcoholConsump'],  # HvyAlcoholConsump (No/Yes)
        indices['AnyHealthcare'],      # AnyHealthcare (No/Yes)
        indices['NoDocbcCost'],        # NoDocbcCost (No/Yes)
        st.session_state["GenHlth"],   # GenHlth (e.g., 1-5 or 1-10 from slider)
        st.session_state['MentHlth'],           # MentHlth (number of days)
        st.session_state['PhysHlth'],           # PhysHlth (number of days)
        indices['DiffWalk'],           # DiffWalk (No/Yes)
        indices['Sex'],                # Sex (Male/Female)
        indices['Age']+1,                # Age group
        indices['Education']+1,          # Education level
        indices['Income']+1              # Income level
    ]
    
    return feature_list





@st.cache_resource()
def diabetes_prediction(new_data):
    loaded_model = load_model("binary_classification_model_for_diabetes.h5")

    # Make predictions using the loaded model
    new_prediction = loaded_model.predict(new_data)
    print(f'Loaded Model Prediction: {new_prediction[0][0]:.4f}')
    return new_prediction[0][0]


column_names = [
    "HighBP",                # HighBP (No)
    "HighChol",              # HighChol (No)
    "Cholcheck",             # Cholcheck (Yes)
    "BMI",                   # BMI (computed)
    "Smoker",                # Smoker (No)
    "Stroke",                # Stroke (No)
    "HeartDiseaseorAttack",  # HeartDiseaseorAttack (No)
    "PhysActivity",          # PhysActivity (Yes)
    "Fruits",                # Fruits (Eats daily)
    "Veggies",               # Veggies (Eats daily)
    "HvyAlcoholConsump",     # HvyAlcoholConsump (No heavy drinking)
    "AnyHealthcare",         # AnyHealthcare (Has healthcare)
    "NoDocbcCost",           # NoDocbcCost (No financial issues)
    "GenHlth",               # GenHlth (Excellent health, scale: 1-5)
    "MentHlth",              # MentHlth (No bad mental health days in last 30 days)
    "PhysHlth",              # PhysHlth (No bad physical health days in last 30 days)
    "DiffWalk",              # DiffWalk (No difficulty walking)
    "Sex",                   # Sex (Male/Female)
    "Age",                   # Age (age group)
    "Education",             # Education level
    "Income"                 # Income level
]



indices = get_selectbox_indices()
# st.write(indices)
# st.write(create_feature_list(indices))
features = create_feature_list(indices)
if st.button("Make a prediction"):
    df = pd.DataFrame([features], columns=column_names)
    st.write(df)
    percentage_of_diabetes =diabetes_prediction(np.array([features]))
    st.write()

    st.write(f"There is a : {percentage_of_diabetes*100}% that you have diabetes")
    progress = st.progress(0)
    percentage_of_diabetes = percentage_of_diabetes *100
    # Simulate progress
    for i in range(int(percentage_of_diabetes)):
        progress.progress(i + 1)
        time.sleep(0.02) 
        
