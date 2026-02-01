import streamlit as st
import pickle
import numpy as np
import os

# --- 1. Modern Page Config ---
st.set_page_config(
    page_title="FutureStock AI",
    page_icon="⚡",
    layout="centered"
)

# --- 2. Custom CSS (Dark & Colorful Theme) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom right, #1a1a2e, #16213e);
        color: #ffffff;
    }
    
    /* Input Fields */
    .stNumberInput > div > div > input {
        background-color: #0f3460;
        color: white;
        border-radius: 10px;
        border: 1px solid #e94560;
    }
    
    /* Headers */
    h1 {
        background: -webkit-linear-gradient(45deg, #00d4ff, #e94560);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* The Predict Button */
    .stButton>button {
        background: linear-gradient(90deg, #e94560, #0f3460);
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0px 0px 20px rgba(233, 69, 96, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 30px rgba(233, 69, 96, 0.6);
    }
    
    /* Result Card */
    .metric-card {
        background-color: #16213e;
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. App Header ---
st.title("⚡ FutureStock AI")
st.markdown("<p style='text-align: center; color: #a0a0a0;'>Enter today's market data to predict tomorrow's price.</p>", unsafe_allow_html=True)

# --- 4. Load Model ---
model_filename = 'Lr_Pipeline.pkl'

if os.path.exists(model_filename):
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
else:
    st.error(f"❌ Model file '{model_filename}' not found. Please place it in the same folder.")
    st.stop()

# --- 5. User Inputs (Organized in Columns) ---
with st.container():
    st.write("### 📊 Daily Indicators")
    
    col1, col2 = st.columns(2)
    with col1:
        open_val = st.number_input("Open Price", value=150.0, step=0.5)
        high_val = st.number_input("High Price", value=155.0, step=0.5)
        vol_val  = st.number_input("Volume", value=5000, step=100)
        
    with col2:
        low_val  = st.number_input("Low Price", value=148.0, step=0.5)
        close_val = st.number_input("Close Price", value=152.0, step=0.5)

    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # --- 6. Prediction Logic ---
    if st.button("🔮 GENERATE PREDICTION"):
        try:
            # Create the array. 
            # NOTE: We try 5 inputs first. If your model was trained on 4, we catch the error.
            features = np.array([[open_val, high_val, low_val, close_val, vol_val]])
            
            # Attempt prediction
            try:
                prediction = model.predict(features)[0]
            except ValueError:
                # Fallback: If model was trained on only 4 columns (Open, High, Low, Volume)
                features_4 = np.array([[open_val, high_val, low_val, vol_val]])
                prediction = model.predict(features_4)[0]
                st.warning("⚠️ Note: Used 4 features (Open, High, Low, Volume) to match your saved model.")

            # Display Result
            st.markdown(f"""
            <div class="metric-card">
                <h2 style="color: #00d4ff; margin:0;">${prediction:,.2f}</h2>
                <p style="color: #e0e0e0; margin:0;">Predicted Price for Tomorrow</p>
            </div>
            """, unsafe_allow_html=True)

            # Simple logic for text feedback
            if prediction > close_val:
                st.markdown("<p style='text-align:center; color:#00ff00; margin-top:10px;'>🚀 Bullish Trend Expected</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='text-align:center; color:#ff4d4d; margin-top:10px;'>📉 Bearish Trend Expected</p>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")