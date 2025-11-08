"""
نظام الترجمة للتطبيق - دعم العربية والإنجليزية
"""

TRANSLATIONS = {
    'en': {
        # Main titles
        'app_title': '🐦 Twitter (X) Sentiment Analyzer',
        'settings': '⚙️ Settings',
        'results': '📊 Results',

        # Settings sidebar
        'search_type': 'Search Type:',
        'search_type_keyword': 'Keyword',
        'search_type_hashtag': 'Hashtag',
        'search_input': 'Enter text:',
        'search_placeholder': 'e.g., AI or #ChatGPT',
        'search_help': 'Enter the word or hashtag to analyze',
        'tweet_count': 'Number of tweets:',
        'tweet_count_help': 'Choose number from {min} to {max}',
        'language': 'Language:',
        'language_help': 'Select the language of tweets',
        'analysis_method': 'Analysis Method:',
        'analysis_method_help': 'TextBlob: Fast\nVADER: Better for English\nBoth: More accurate but slower',
        'method_textblob': 'TextBlob (Faster)',
        'method_vader': 'VADER (Balanced)',
        'method_both': 'Both (Most Accurate)',
        'start_analysis': '🚀 Start Analysis',
        'footer': 'By: Twitter Sentiment Analyzer<br>Phase 1 - v1.0',

        # Language options
        'lang_arabic': 'Arabic',
        'lang_english': 'English',
        'lang_all': 'All',

        # Welcome page
        'welcome_title': '👋 Welcome to Twitter Sentiment Analyzer!',
        'how_to_use': '**How to Use:**',
        'step1': '1. Choose search type (keyword or hashtag)',
        'step2': '2. Enter the text to analyze',
        'step3': '3. Select number of tweets and language',
        'step4': '4. Click "Start Analysis"',
        'features': '**Features:**',
        'feature1': '- 📊 Interactive charts',
        'feature2': '- 🎯 Accurate sentiment analysis',
        'feature3': '- 📝 Keyword extraction',
        'feature4': '- 📈 Timeline analysis',
        'feature5': '- 💾 Export results',
        'metrics_languages': 'Language Support',
        'metrics_languages_delta': 'Arabic & English',
        'metrics_methods': 'Analysis Methods',
        'metrics_methods_delta': 'TextBlob, VADER, Both',
        'metrics_accuracy': 'Analysis Accuracy',
        'metrics_accuracy_delta': 'Improvable',

        # Status messages
        'fetching_tweets': '⏳ Fetching tweets from Twitter...',
        'cleaning_text': '🧹 Cleaning text...',
        'analyzing_sentiment': '🤖 Analyzing sentiments...',
        'tweets_fetched': '✅ Successfully fetched {count} tweets!',
        'no_tweets_found': '⚠️ No tweets found. Try another search term.',

        # Error messages
        'error_no_env': '❌ .env file not found!',
        'error_env_instructions': '''
        Please create a .env file using .env.example as a template and add your Twitter API keys.

        Steps to get the keys:
        1. Visit https://developer.twitter.com/en/portal/dashboard
        2. Create a new project
        3. Copy the keys to .env file
        ''',
        'error_validation': '❌ Please enter search text',
        'error_occurred': '❌ Error occurred: {error}',
        'error_api_connection': '❌ Failed to connect to Twitter API',
        'error_timeout': '⏰ Request timeout. Please try again with fewer tweets.',

        # Results tabs
        'tab_distribution': '📊 Distribution',
        'tab_keywords': '📝 Top Keywords',
        'tab_timeline': '📈 Timeline',
        'tab_tweets': '💬 Tweets',
        'tab_export': '📥 Export',

        # Metrics
        'total_tweets': 'Total Tweets',
        'positive': 'Positive 😊',
        'negative': 'Negative 😞',
        'neutral': 'Neutral 😐',

        # Charts
        'chart_sentiment_dist': 'Sentiment Distribution',
        'chart_word_freq': 'Most Frequent Words',
        'chart_timeline': 'Sentiment Evolution Over Time',
        'no_keywords': 'No enough keywords found',
        'no_timeline_data': 'Not enough timeline data to display',
        'timeline_error': 'Could not create timeline chart: {error}',

        # Tweets table
        'filter_sentiment': 'Filter by sentiment:',
        'showing_tweets': 'Showing {filtered} of {total} tweets',

        # Export
        'export_title': 'Export Results',
        'export_full': '📥 Download Full Results (CSV)',
        'export_stats': '📊 Download Statistics (CSV)',
        'export_success': '✅ You can now download the results in CSV format',

        # Sentiment labels
        'sentiment_positive': 'Positive',
        'sentiment_negative': 'Negative',
        'sentiment_neutral': 'Neutral',

        # UI
        'app_language': 'App Language',
    },
    'ar': {
        # Main titles
        'app_title': '🐦 محلل مشاعر تويتر (X)',
        'settings': '⚙️ الإعدادات',
        'results': '📊 النتائج',

        # Settings sidebar
        'search_type': 'نوع البحث:',
        'search_type_keyword': 'كلمة مفتاحية',
        'search_type_hashtag': 'هاشتاغ',
        'search_input': 'أدخل النص:',
        'search_placeholder': 'مثال: الذكاء الاصطناعي أو #AI',
        'search_help': 'أدخل الكلمة أو الهاشتاغ المراد تحليله',
        'tweet_count': 'عدد التغريدات:',
        'tweet_count_help': 'اختر عدد التغريدات من {min} إلى {max}',
        'language': 'اللغة:',
        'language_help': 'حدد لغة التغريدات المراد جلبها',
        'analysis_method': 'طريقة التحليل:',
        'analysis_method_help': 'TextBlob: سريع وبسيط\nVADER: أفضل للغة الإنجليزية\nكلاهما: أدق لكن أبطأ',
        'method_textblob': 'TextBlob (أسرع)',
        'method_vader': 'VADER (متوازن)',
        'method_both': 'كلاهما (أدق)',
        'start_analysis': '🚀 ابدأ التحليل',
        'footer': 'بواسطة: Twitter Sentiment Analyzer<br>المرحلة الأولى - v1.0',

        # Language options
        'lang_arabic': 'العربية',
        'lang_english': 'الإنجليزية',
        'lang_all': 'الكل',

        # Welcome page
        'welcome_title': '👋 مرحباً بك في محلل مشاعر تويتر!',
        'how_to_use': '**كيفية الاستخدام:**',
        'step1': '1. اختر نوع البحث (كلمة مفتاحية أو هاشتاغ)',
        'step2': '2. أدخل النص المراد تحليله',
        'step3': '3. حدد عدد التغريدات واللغة',
        'step4': '4. اضغط على "ابدأ التحليل"',
        'features': '**المميزات:**',
        'feature1': '- 📊 رسوم بيانية تفاعلية',
        'feature2': '- 🎯 تحليل دقيق للمشاعر',
        'feature3': '- 📝 استخراج الكلمات المفتاحية',
        'feature4': '- 📈 تحليل التطور الزمني',
        'feature5': '- 💾 تصدير النتائج',
        'metrics_languages': 'دعم اللغات',
        'metrics_languages_delta': 'العربية والإنجليزية',
        'metrics_methods': 'طرق التحليل',
        'metrics_methods_delta': 'TextBlob, VADER, كلاهما',
        'metrics_accuracy': 'دقة التحليل',
        'metrics_accuracy_delta': 'قابلة للتحسين',

        # Status messages
        'fetching_tweets': '⏳ جاري جلب التغريدات من Twitter...',
        'cleaning_text': '🧹 جاري تنظيف النصوص...',
        'analyzing_sentiment': '🤖 جاري تحليل المشاعر...',
        'tweets_fetched': '✅ تم جلب {count} تغريدة بنجاح!',
        'no_tweets_found': '⚠️ لم يتم العثور على أي تغريدات. جرب كلمة بحث أخرى.',

        # Error messages
        'error_no_env': '❌ ملف .env غير موجود!',
        'error_env_instructions': '''
        الرجاء إنشاء ملف .env باستخدام .env.example كنموذج وإضافة مفاتيح Twitter API الخاصة بك.

        خطوات الحصول على المفاتيح:
        1. زيارة https://developer.twitter.com/en/portal/dashboard
        2. إنشاء مشروع جديد
        3. نسخ المفاتيح إلى ملف .env
        ''',
        'error_validation': '❌ الرجاء إدخال نص للبحث',
        'error_occurred': '❌ حدث خطأ: {error}',
        'error_api_connection': '❌ فشل الاتصال بـ Twitter API',
        'error_timeout': '⏰ انتهى الوقت المحدد. الرجاء المحاولة بعدد أقل من التغريدات.',

        # Results tabs
        'tab_distribution': '📊 التوزيع',
        'tab_keywords': '📝 الكلمات الأكثر تكراراً',
        'tab_timeline': '📈 التطور الزمني',
        'tab_tweets': '💬 التغريدات',
        'tab_export': '📥 التصدير',

        # Metrics
        'total_tweets': 'إجمالي التغريدات',
        'positive': 'إيجابي 😊',
        'negative': 'سلبي 😞',
        'neutral': 'محايد 😐',

        # Charts
        'chart_sentiment_dist': 'توزيع المشاعر',
        'chart_word_freq': 'الكلمات الأكثر تكراراً',
        'chart_timeline': 'تطور المشاعر عبر الزمن',
        'no_keywords': 'لم يتم العثور على كلمات مفتاحية كافية',
        'no_timeline_data': 'لا توجد بيانات زمنية كافية للعرض',
        'timeline_error': 'تعذر إنشاء الرسم الزمني: {error}',

        # Tweets table
        'filter_sentiment': 'تصفية حسب المشاعر:',
        'showing_tweets': 'عرض {filtered} من {total} تغريدة',

        # Export
        'export_title': 'تصدير النتائج',
        'export_full': '📥 تحميل النتائج الكاملة (CSV)',
        'export_stats': '📊 تحميل الإحصائيات (CSV)',
        'export_success': '✅ يمكنك الآن تحميل النتائج بتنسيق CSV لاستخدامها في برامج أخرى',

        # Sentiment labels
        'sentiment_positive': 'إيجابي',
        'sentiment_negative': 'سلبي',
        'sentiment_neutral': 'محايد',

        # UI
        'app_language': 'لغة التطبيق',
    }
}


def get_text(key, lang='en', **kwargs):
    """
    الحصول على النص المترجم

    Args:
        key: مفتاح النص
        lang: اللغة ('en' أو 'ar')
        **kwargs: متغيرات للتنسيق

    Returns:
        str: النص المترجم
    """
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

    # تنسيق النص إذا كانت هناك متغيرات
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text


def get_direction(lang='en'):
    """
    الحصول على اتجاه النص

    Args:
        lang: اللغة

    Returns:
        str: 'rtl' أو 'ltr'
    """
    return 'rtl' if lang == 'ar' else 'ltr'
