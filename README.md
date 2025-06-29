# DEFENSE SCOPE 🛰️

**DEFENSE SCOPE** is an AI-powered dashboard that fetches, analyzes, and visualizes real-time global defense news.

Built by a student passionate about space, AI, and national security, this tool combines:
- 💬 Sentiment analysis
- 🌍 Region tagging
- ⚠️ Threat alert detection
- ☁️ Word cloud of trending terms
- 🗺️ Interactive map of global events

### 🔧 Features

- **Live News Fetching**: Uses NewsAPI to pull real-time defense/military-related headlines from around the world.
- **AI Sentiment Analysis**: Classifies each headline as Positive, Negative, or Neutral.
- **Region Identification**: Tags each news item with its geopolitical region.
- **Threat Detection**: Flags articles involving conflict-related keywords.
- **Word Cloud**: Highlights trending keywords visually.
- **Map View**: Shows geo-located news on a world map using `pydeck`.

### 🚀 Built With
- [Streamlit](https://streamlit.io/) – UI Framework
- [TextBlob](https://textblob.readthedocs.io/en/dev/) – Sentiment analysis
- [NewsAPI](https://newsapi.org/) – News aggregation
- [Pydeck](https://deckgl.readthedocs.io/en/latest/) – Interactive maps
- [WordCloud](https://github.com/amueller/word_cloud) – Visual NLP



### 📦 Run Locally

```bash
git clone https://github.com/your-username/defense-scope
cd defense-scope
pip install -r requirements.txt
streamlit run app.py
