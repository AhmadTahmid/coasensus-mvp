import streamlit as st
import requests
import pandas as pd

# 1. Page Config (The "Look")
st.set_page_config(page_title="Coasensus", page_icon="🌐", layout="centered")

# 2. Header
st.title("🌐 Coasensus")
st.subheader("The Signal in the Noise.")
st.write("Aggregated probabilities from the world's leading prediction markets.")
st.divider()

# 3. The Engine (Fetching Data from Polymarket)
@st.cache_data(ttl=60) # Updates every 60 seconds
def fetch_markets():
    # We use the 'Gamma' API from Polymarket which is free and public
    url = "https://gamma-api.polymarket.com/events?closed=false&limit=10&order=volume24hr"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error connecting to the Lighthouse: {e}")
        return []

# 4. Display Logic
markets = fetch_markets()

if markets:
    for event in markets:
        # Only show events that have markets
        if not event.get('markets'):
            continue
            
        market = event['markets'][0] # Grab the main market for this event
        title = event.get('title', 'Unknown Event')
        
        # Extract Probability (The "Coasensus")
        # Polymarket prices are 0.00 to 1.00. We convert to %.
        try:
            raw_price = float(market.get('group', [{}])[0].get('outcomePrices', [0])[0])
            probability = round(raw_price * 100, 1)
        except:
            # Fallback if structure is different
            continue

        # Visual Card
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {title}")
                st.caption(f"Source: Polymarket | Volume: ${round(float(event.get('volume', 0))/1000000, 2)}M")
            with col2:
                st.metric(label="Probability", value=f"{probability}%")
            
            st.divider()
else:
    st.write("Waiting for signal...")

# 5. Footer
st.markdown("---")
st.caption("© 2026 Coasensus. Built for the Public Good.")
