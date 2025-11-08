# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-08

### Added
- **Multi-language UI support** - Switch between English and Arabic
- **Intelligent timeout system** - Prevents hanging (30-120s based on tweet count)
- **Progress indicators** - Real-time feedback with progress bar and status messages
- **Comprehensive translations** - Full translation system in `config/translations.py`
- **Smaller sidebar fonts** - Improved text display and wrapping
- **Enhanced error messages** - More detailed and helpful error descriptions

### Changed
- **Default language** - Changed from Arabic to English
- **UI font sizes** - Reduced for better space utilization
- **Timeout behavior** - Now shows elapsed time and suggestions on timeout
- **CSS styling** - Improved RTL/LTR support based on language

### Fixed
- **Long text truncation** - Fixed sidebar text being cut off
- **Timeout handling** - No more indefinite hangs during API calls
- **CORS warnings** - Fixed Streamlit configuration warnings
- **Config errors** - Removed deprecated config options

### Technical
- Added `ThreadPoolExecutor` for timeout management
- Implemented `fetch_with_timeout()` function
- Enhanced `apply_custom_css()` with dynamic direction
- Improved error handling in `perform_analysis()`

## [1.0.0] - 2025-11-06

### Added
- Initial release
- Twitter API integration via Tweepy
- TextBlob sentiment analysis
- VADER sentiment analysis
- Streamlit web interface
- Interactive Plotly visualizations
- Text cleaning and preprocessing
- Keyword extraction
- Timeline analysis
- CSV export functionality
- Comprehensive logging system
- Error handling utilities

### Features
- Search by keyword or hashtag
- Support for Arabic and English tweets
- Real-time sentiment analysis
- Multiple visualization types:
  - Pie chart for sentiment distribution
  - Bar chart for word frequency
  - Timeline chart for sentiment evolution
  - Scatter plot for engagement vs sentiment
- Configurable tweet count (50-1000)
- Language filtering (Arabic/English/All)
- Analysis method selection (TextBlob/VADER/Both)

### Documentation
- Comprehensive README
- Quick start guide
- Installation instructions
- Project summary
- Contributing guidelines
- MIT License

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|------------|
| 1.1.0 | 2025-11-08 | Multi-language UI, Smart timeout, Progress indicators |
| 1.0.0 | 2025-11-06 | Initial release with core features |

---

## Upcoming Features

See [Future Enhancements](README.md#-future-enhancements) in README for planned features.

### Planned for v1.2.0
- [ ] User account analysis
- [ ] Single tweet analysis
- [ ] Advanced time range filtering
- [ ] Improved Arabic sentiment accuracy
- [ ] Caching for better performance

### Planned for v2.0.0
- [ ] Deep learning models (BERT, transformers)
- [ ] Topic modeling
- [ ] Sarcasm detection
- [ ] Multi-language expansion (French, Spanish)
- [ ] RESTful API
- [ ] Docker support
