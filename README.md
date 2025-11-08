# 🐦 Twitter Sentiment Analyzer

A professional sentiment analysis tool for Twitter (X) with multi-language support and interactive visualizations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

## ✨ Key Features

- 🌍 **Multi-language UI** - English & Arabic interface
- 🔍 **Flexible Search** - Keywords or hashtags
- 🤖 **Dual Analysis** - TextBlob & VADER engines
- 📊 **Interactive Charts** - Real-time Plotly visualizations
- ⏱️ **Smart Timeout** - Automatic timeout (30-120s)
- 📈 **Timeline Analysis** - Sentiment evolution tracking
- 💾 **Export** - Download results as CSV

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Add your Twitter API keys to .env

# Run application
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## 📖 Usage

1. Choose language (English/Arabic)
2. Select search type (Keyword/Hashtag)
3. Enter search query
4. Configure tweet count & language
5. Click "Start Analysis"
6. Explore results & download data

## 🔑 Twitter API Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project & app
3. Generate API keys
4. Add keys to `.env` file:

```env
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## 📊 Analysis Methods

| Method | Speed | Best For | Accuracy |
|--------|-------|----------|----------|
| TextBlob | ⚡ Fast | General use | Good |
| VADER | 🚀 Medium | Social media | Very Good |
| Both | 🐢 Slower | Critical analysis | Excellent |

## 🛠️ Project Structure

```
twitter-sentiment-analyzer/
├── app.py                 # Main Streamlit app
├── config/
│   ├── settings.py       # Configuration
│   └── translations.py   # Multi-language support
├── src/
│   ├── data_fetcher.py   # Twitter API integration
│   ├── text_cleaner.py   # Text preprocessing
│   ├── sentiment_analyzer.py  # Analysis engine
│   └── visualizer.py     # Charts & visualizations
└── utils/
    ├── error_handler.py  # Error management
    └── logger.py         # Logging system
```

## 📝 Requirements

- Python 3.8+
- Twitter Developer Account
- Dependencies in `requirements.txt`

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Priority areas:**
- Improve Arabic sentiment accuracy
- Add more languages
- Implement deep learning models
- Enhance visualizations

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

Built with: [Tweepy](https://www.tweepy.org/) • [Streamlit](https://streamlit.io/) • [Plotly](https://plotly.com/) • [TextBlob](https://textblob.readthedocs.io/) • [VADER](https://github.com/cjhutto/vaderSentiment)

## 📈 Version

**v1.1.0** - Multi-language support, smart timeout, progress indicators

---

⭐ **Star this repo if you find it useful!**

Made with ❤️ for the global community
