"""
Streamlit App for Twitter Sentiment Analysis
تطبيق Streamlit لتحليل مشاعر التغريدات
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

# Import components
from src.data_fetcher import TwitterDataFetcher
from src.text_cleaner import TextCleaner
from src.sentiment_analyzer import SentimentAnalyzer
from src.visualizer import SentimentVisualizer
from utils.error_handler import validate_input, handle_api_error
from utils.logger import app_logger
from config.settings import (
    PAGE_TITLE, PAGE_ICON, LAYOUT,
    MIN_TWEETS, MAX_TWEETS, DEFAULT_TWEETS,
    LANGUAGE_MAP
)
from config.translations import get_text, get_direction

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state"""
    if 'app_lang' not in st.session_state:
        st.session_state.app_lang = 'en'  # Default to English
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None
    if 'stats' not in st.session_state:
        st.session_state.stats = None
    if 'word_freq_df' not in st.session_state:
        st.session_state.word_freq_df = None


def apply_custom_css(lang='en'):
    """Apply custom CSS based on language"""
    direction = get_direction(lang)

    st.markdown(f"""
    <style>
        .main-header {{
            text-align: center;
            color: #1DA1F2;
            padding: 1rem 0;
            direction: {direction};
        }}
        .stAlert {{
            direction: {direction};
        }}
        div[data-testid="stMetricValue"] {{
            font-size: 1.8rem;
        }}
        /* Smaller font in sidebar */
        .css-1d391kg, section[data-testid="stSidebar"] {{
            font-size: 0.9rem;
        }}
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stTextInput label,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stSlider label {{
            font-size: 0.85rem !important;
        }}
        /* Make sidebar text wrap properly */
        section[data-testid="stSidebar"] {{
            word-wrap: break-word;
        }}
    </style>
    """, unsafe_allow_html=True)


def check_env_file(lang='en'):
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        st.error(get_text('error_no_env', lang) + "\n\n" + get_text('error_env_instructions', lang))
        return False
    return True


def check_api_connection():
    """Test API connection with timeout"""
    try:
        with st.spinner("Testing API connection..."):
            fetcher = TwitterDataFetcher()
            if fetcher.client:
                return True, "✅ API connection successful"
            return False, "❌ Failed to initialize API client"
    except Exception as e:
        return False, f"❌ API Error: {str(e)}"


def fetch_with_timeout(fetcher, search_type, query, count, lang_code, timeout=60):
    """Fetch tweets with timeout"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        if search_type == "hashtag":
            future = executor.submit(fetcher.fetch_by_hashtag, query, count, lang_code)
        else:
            future = executor.submit(fetcher.fetch_by_keyword, query, count, lang_code)

        try:
            result = future.result(timeout=timeout)
            return result, None
        except FutureTimeoutError:
            return None, "timeout"
        except Exception as e:
            return None, str(e)


def main():
    """Main application function"""

    # Initialize session state
    init_session_state()

    lang = st.session_state.app_lang

    # Apply CSS
    apply_custom_css(lang)

    # Main header
    st.markdown(f'<h1 class="main-header">{get_text("app_title", lang)}</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Check .env file
    if not check_env_file(lang):
        st.stop()

    # Sidebar for settings
    with st.sidebar:
        st.title(get_text('settings', lang))

        # Language selector at top
        col1, col2 = st.columns([3, 1])
        with col1:
            app_language = st.selectbox(
                get_text('app_language', lang),
                ['English', 'العربية'],
                index=0 if lang == 'en' else 1,
                key='lang_selector'
            )

        # Update language if changed
        new_lang = 'en' if app_language == 'English' else 'ar'
        if new_lang != st.session_state.app_lang:
            st.session_state.app_lang = new_lang
            st.rerun()

        st.markdown("---")

        # Search type
        search_type_options = [
            get_text('search_type_keyword', lang),
            get_text('search_type_hashtag', lang)
        ]
        search_type = st.radio(
            get_text('search_type', lang),
            search_type_options,
            help=get_text('search_help', lang)
        )

        # Query input
        query = st.text_input(
            get_text('search_input', lang),
            placeholder=get_text('search_placeholder', lang),
            help=get_text('search_help', lang)
        )

        # Tweet count
        tweet_count = st.slider(
            get_text('tweet_count', lang),
            min_value=MIN_TWEETS,
            max_value=MAX_TWEETS,
            value=DEFAULT_TWEETS,
            step=10,
            help=get_text('tweet_count_help', lang, min=MIN_TWEETS, max=MAX_TWEETS)
        )

        # Language selection
        language_options = [
            get_text('lang_english', lang),
            get_text('lang_arabic', lang),
            get_text('lang_all', lang)
        ]
        language = st.selectbox(
            get_text('language', lang),
            language_options,
            help=get_text('language_help', lang)
        )

        # Analysis method
        method_options = [
            get_text('method_textblob', lang),
            get_text('method_vader', lang),
            get_text('method_both', lang)
        ]
        analysis_method = st.selectbox(
            get_text('analysis_method', lang),
            method_options,
            help=get_text('analysis_method_help', lang)
        )

        st.markdown("---")

        # Analysis button
        analyze_button = st.button(
            get_text('start_analysis', lang),
            type="primary",
            use_container_width=True
        )

        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; font-size: 11px; color: gray;'>
        {get_text('footer', lang)}
        </div>
        """, unsafe_allow_html=True)

    # Main area
    if not analyze_button:
        show_welcome_page(lang)
    else:
        # Convert search type
        search_type_en = 'hashtag' if search_type == search_type_options[1] else 'keyword'

        # Convert language
        lang_map = {
            language_options[0]: 'en',
            language_options[1]: 'ar',
            language_options[2]: 'all'
        }
        selected_lang = lang_map[language]

        perform_analysis(query, tweet_count, search_type_en, selected_lang, analysis_method, lang)


def show_welcome_page(lang='en'):
    """Display welcome page"""
    st.info(f"""
    ### {get_text('welcome_title', lang)}

    {get_text('how_to_use', lang)}
    {get_text('step1', lang)}
    {get_text('step2', lang)}
    {get_text('step3', lang)}
    {get_text('step4', lang)}

    {get_text('features', lang)}
    {get_text('feature1', lang)}
    {get_text('feature2', lang)}
    {get_text('feature3', lang)}
    {get_text('feature4', lang)}
    {get_text('feature5', lang)}
    """)

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            get_text('metrics_languages', lang),
            "2+",
            delta=get_text('metrics_languages_delta', lang)
        )
    with col2:
        st.metric(
            get_text('metrics_methods', lang),
            "3",
            delta=get_text('metrics_methods_delta', lang)
        )
    with col3:
        st.metric(
            get_text('metrics_accuracy', lang),
            "70%+",
            delta=get_text('metrics_accuracy_delta', lang)
        )


def perform_analysis(query, tweet_count, search_type, language, analysis_method, lang='en'):
    """
    Perform complete analysis with timeout and progress indicators
    """
    # Validate input
    valid, message = validate_input(query, tweet_count)
    if not valid:
        st.error(message)
        return

    try:
        # Progress container
        progress_container = st.container()
        status_text = st.empty()
        progress_bar = st.progress(0)

        # 1. Fetch tweets with timeout
        status_text.text(get_text('fetching_tweets', lang))
        progress_bar.progress(10)

        start_time = time.time()
        fetcher = TwitterDataFetcher()

        # Determine timeout based on tweet count
        timeout = min(120, 30 + (tweet_count // 10))  # 30s base + 1s per 10 tweets, max 120s

        lang_code = LANGUAGE_MAP.get(language, 'all')
        tweets_df, error = fetch_with_timeout(fetcher, search_type, query, tweet_count, lang_code, timeout)

        elapsed = time.time() - start_time

        if error == "timeout":
            st.error(get_text('error_timeout', lang))
            st.warning(f"⏱️ Timeout after {elapsed:.1f}s. Try with fewer tweets or check your internet connection.")
            progress_bar.empty()
            status_text.empty()
            return
        elif error:
            st.error(get_text('error_occurred', lang, error=error))
            progress_bar.empty()
            status_text.empty()
            return

        if tweets_df is None or tweets_df.empty:
            st.warning(get_text('no_tweets_found', lang))
            progress_bar.empty()
            status_text.empty()
            return

        st.success(get_text('tweets_fetched', lang, count=len(tweets_df)))
        progress_bar.progress(30)

        # 2. Clean text
        status_text.text(get_text('cleaning_text', lang))
        cleaner = TextCleaner()
        tweets_df = cleaner.clean_dataframe(tweets_df)
        progress_bar.progress(50)

        # 3. Analyze sentiments
        status_text.text(get_text('analyzing_sentiment', lang))
        analyzer = SentimentAnalyzer()

        # Determine method
        if get_text('method_textblob', lang) in analysis_method:
            method = 'textblob'
        elif get_text('method_vader', lang) in analysis_method:
            method = 'vader'
        else:
            method = 'both'

        tweets_df = analyzer.analyze_dataframe(tweets_df, method=method)
        stats = analyzer.get_sentiment_statistics(tweets_df)
        word_freq_df = cleaner.get_word_frequency(tweets_df, top_n=20)

        progress_bar.progress(90)

        # Save results
        st.session_state.results_df = tweets_df
        st.session_state.stats = stats
        st.session_state.word_freq_df = word_freq_df
        st.session_state.analysis_done = True

        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        # 4. Display results
        display_results(tweets_df, stats, word_freq_df, query, lang)

    except Exception as e:
        app_logger.error(f"Analysis error: {str(e)}")
        st.error(get_text('error_occurred', lang, error=str(e)))


def display_results(df, stats, word_freq_df, query, lang='en'):
    """Display analysis results"""

    st.markdown("---")
    st.subheader(get_text('results', lang))

    # 1. Metrics cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(get_text('total_tweets', lang), stats['total'])

    with col2:
        st.metric(
            get_text('positive', lang),
            f"{stats['positive']} ({stats['positive_pct']}%)"
        )

    with col3:
        st.metric(
            get_text('negative', lang),
            f"{stats['negative']} ({stats['negative_pct']}%)"
        )

    with col4:
        st.metric(
            get_text('neutral', lang),
            f"{stats['neutral']} ({stats['neutral_pct']}%)"
        )

    st.markdown("---")

    # 2. Tabs for visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        get_text('tab_distribution', lang),
        get_text('tab_keywords', lang),
        get_text('tab_timeline', lang),
        get_text('tab_tweets', lang),
        get_text('tab_export', lang)
    ])

    visualizer = SentimentVisualizer()

    with tab1:
        st.subheader(get_text('chart_sentiment_dist', lang))
        sentiment_counts = df['sentiment'].value_counts()
        fig = visualizer.plot_sentiment_pie(sentiment_counts, get_text('chart_sentiment_dist', lang))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(get_text('chart_word_freq', lang))
        if not word_freq_df.empty:
            fig = visualizer.plot_word_frequency_bar(word_freq_df, get_text('chart_word_freq', lang), top_n=15)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(get_text('no_keywords', lang))

    with tab3:
        st.subheader(get_text('chart_timeline', lang))
        try:
            analyzer = SentimentAnalyzer()
            time_sentiment = analyzer.analyze_sentiment_over_time(df)
            if not time_sentiment.empty:
                fig = visualizer.plot_sentiment_timeline(time_sentiment, get_text('chart_timeline', lang))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(get_text('no_timeline_data', lang))
        except Exception as e:
            st.warning(get_text('timeline_error', lang, error=str(e)))

    with tab4:
        st.subheader(get_text('tab_tweets', lang))

        # Sentiment filter
        sentiment_options = [
            get_text('sentiment_positive', lang),
            get_text('sentiment_negative', lang),
            get_text('sentiment_neutral', lang)
        ]

        # Map display names to actual values
        sentiment_map = {
            get_text('sentiment_positive', lang): 'إيجابي',
            get_text('sentiment_negative', lang): 'سلبي',
            get_text('sentiment_neutral', lang): 'محايد'
        }

        selected_sentiments = st.multiselect(
            get_text('filter_sentiment', lang),
            options=sentiment_options,
            default=sentiment_options
        )

        # Convert back to original sentiment values
        filter_values = [sentiment_map[s] for s in selected_sentiments]
        filtered_df = df[df['sentiment'].isin(filter_values)]

        # Display table
        display_columns = ['text', 'sentiment', 'likes', 'retweets', 'created_at']
        available_columns = [col for col in display_columns if col in filtered_df.columns]

        st.dataframe(
            filtered_df[available_columns],
            use_container_width=True,
            height=400
        )

        st.info(get_text('showing_tweets', lang, filtered=len(filtered_df), total=len(df)))

    with tab5:
        st.subheader(get_text('export_title', lang))

        col1, col2 = st.columns(2)

        with col1:
            # Export full results
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label=get_text('export_full', lang),
                data=csv,
                file_name=f"sentiment_analysis_{query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            # Export statistics
            stats_df = pd.DataFrame([stats])
            stats_csv = stats_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label=get_text('export_stats', lang),
                data=stats_csv,
                file_name=f"stats_{query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.success(get_text('export_success', lang))


if __name__ == "__main__":
    main()
