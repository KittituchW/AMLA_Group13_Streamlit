# import streamlit as st
# import requests

# # === CHANGE THESE TWO VALUES ===
# COIN = "ETHUSD"  # your coin name
# API_URL = "https://amla-at3-fastapi-latest.onrender.com"  # your FastAPI endpoint

# # --- Simple API call example ---
# st.markdown(f"### 🔮 Prediction for {COIN}")

# price = st.number_input("Enter current price", value=3200.0)

# if st.button("Get Prediction"):
#     try:
#         res = requests.get(f"{API_URL}/{COIN}", params={"price": price})
#         if res.status_code == 200:
#             data = res.json()
#             st.success("✅ Prediction received!")
#             st.metric("Predicted HIGH", f"${data['predictedHigh']:,.2f}")
#             st.metric("Confidence", f"{data['confidence']}%")
#             st.caption(f"Model: {data['modelName']}")
#         else:
#             st.error(f"❌ API error: {res.status_code}")
#     except Exception as e:
#         st.error(f"⚠️ Could not connect to API: {e}")


API_URL = "https://amla-at3-fastapi-latest.onrender.com"
MODEL_NAME = "LinearRegressionModel"
