import streamlit as st
import pandas as pd
import requests
import json
from textblob import TextBlob
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pydeck as pdk

# ---------- Page Config ----------
st.set_page_config(page_title="DEFENSE SCOPE", layout="wide")

# ---------- App Title ----------
st.title("🛰️ DEFENSE SCOPE – Global Defense News Sentiment Tracker")

# ---------- Country Coordinates ----------
country_coords = {
    "India": [20.5937, 78.9629],
    "China": [35.8617, 104.1954],
    "USA": [37.0902, -95.7129],
    "Russia": [61.5240, 105.3188],
    "Pakistan": [30.3753, 69.3451],
    "Japan": [36.2048, 138.2529],
    "Iran": [32.4279, 53.6880],
    "Global": [0, 0]
}

# ---------- Sentiment Analysis ----------
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.polarity > 0.1:
        return "Positive"
    elif analysis.polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# ---------- Region Tagging ----------
def get_region(text):
    if "India" in text: return "India"
    elif "China" in text: return "China"
    elif "USA" in text: return "USA"
    elif "Russia" in text: return "Russia"
    else: return "Global"

# ---------- Threat Detection ----------
def is_threat(text):
    threat_keywords = ["missile", "attack", "invasion", "explosion", "strike", "conflict", "border", "test launch"]
    text = text.lower()
    return any(keyword in text for keyword in threat_keywords)

# ---------- Fetch + Process News ----------
API_KEY = "ed55a22b0d5d42f1978363b89918b62b"

def load_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=defense OR military OR war&"
        f"language=en&"
        f"pageSize=100&"
        f"sortBy=publishedAt&"
        f"apiKey={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        st.error("❌ Failed to fetch live news.")
        return pd.DataFrame()
    
    raw_data = response.json().get("articles", [])

    processed = []
for article in raw_data:
    title = article.get("title") or ""
    description = article.get("description") or ""
    source_data = article.get("source", {})
    source = source_data.get("name") if isinstance(source_data, dict) else "Unknown"
    date = article.get("publishedAt", "")[:10]

    full_text = str(title) + " " + str(description)

    sentiment = get_sentiment(full_text)
    region = get_region(full_text)
    threat = "⚠️ Yes" if is_threat(full_text) else "No"
    lat, lon = country_coords.get(region, [0, 0])

    processed.append({
        "Title": title,
        "Source": source,
        "Date": date,
        "Region": region,
        "Sentiment": sentiment,
        "Threat": threat,
        "lat": lat,
        "lon": lon
    })


return pd.DataFrame(processed)

# ---------- Sidebar Refresh Button ----------
st.sidebar.markdown("### 🔄 Manual Refresh")
if st.sidebar.button("Fetch Latest News"):
    st.session_state['df'] = load_news()
    st.sidebar.success("✅ News updated!")

if 'df' not in st.session_state:
    st.session_state['df'] = load_news()

df = st.session_state['df']
st.sidebar.markdown(f"🕒 Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ---------- Sentiment Pie Chart ----------
st.subheader("🧠 Sentiment Overview")
sentiment_counts = df['Sentiment'].value_counts()
fig1 = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, title="Sentiment Distribution")
st.plotly_chart(fig1, use_container_width=True)

# ---------- Region Bar Chart ----------
st.subheader("🌍 Region-Wise Distribution")
region_counts = df['Region'].value_counts()
fig2 = px.bar(x=region_counts.index, y=region_counts.values, title="Articles by Region", color=region_counts.index)
st.plotly_chart(fig2, use_container_width=True)

# ---------- Threat Highlighted Table ----------
st.subheader("📰 Recent Headlines (⚠️ = Potential Threat)")
def highlight_threat(row):
    if row["Threat"] == "⚠️ Yes":
        return ['background-color: #ffcccc']*len(row)
    else:
        return ['']*len(row)

st.dataframe(df.style.apply(highlight_threat, axis=1), use_container_width=True)

# ---------- Word Cloud ----------
st.subheader("☁️ Keyword Word Cloud")
all_text = " ".join(df["Title"])
wc = WordCloud(width=1200, height=500, background_color="white").generate(all_text)
fig, ax = plt.subplots(figsize=(12, 5))
ax.imshow(wc, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# ---------- Map ----------
st.subheader("🗺️ News Source Map")
map_df = df[["lat", "lon", "Title", "Threat"]].copy()
map_df["Threat_Level"] = map_df["Threat"].apply(lambda x: 100 if x == "⚠️ Yes" else 30)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_fill_color='[200, 30, 0, Threat_Level]',
            get_radius=500000,
        ),
    ],
))
