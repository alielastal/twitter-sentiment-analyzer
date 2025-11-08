"""
جلب البيانات من Twitter (X) API
"""
import tweepy
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from utils.logger import app_logger
from utils.error_handler import TwitterAPIError, handle_api_error
from config.settings import MAX_TWEETS

# تحميل المتغيرات البيئية
load_dotenv()


class TwitterDataFetcher:
    """فئة لجلب البيانات من Twitter API"""

    def __init__(self):
        """تهيئة الاتصال بـ Twitter API"""
        self.client = None
        self.api = None
        self._setup_api()

    def _setup_api(self):
        """
        إعداد الاتصال بـ Twitter API
        """
        try:
            # جلب المفاتيح من المتغيرات البيئية
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

            if not bearer_token:
                raise TwitterAPIError("مفاتيح API غير موجودة. تأكد من ملف .env")

            # إنشاء Client (API v2)
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )

            app_logger.info("تم الاتصال بنجاح بـ Twitter API")

        except Exception as e:
            app_logger.error(f"فشل الاتصال بـ Twitter API: {str(e)}")
            raise TwitterAPIError(f"فشل الاتصال: {str(e)}")

    def fetch_tweets(self, query, count=100, search_type='keyword', lang='all'):
        """
        جلب التغريدات حسب نوع البحث

        Args:
            query: نص البحث أو الهاشتاغ
            count: عدد التغريدات المطلوبة
            search_type: نوع البحث ('keyword' أو 'hashtag')
            lang: اللغة ('ar', 'en', 'all')

        Returns:
            DataFrame: بيانات التغريدات
        """
        try:
            # تنسيق الاستعلام
            if search_type == 'hashtag':
                if not query.startswith('#'):
                    query = f"#{query}"

            # إضافة فلتر اللغة
            if lang != 'all':
                query = f"{query} lang:{lang}"

            # إزالة الـ retweets للحصول على محتوى أصلي
            query = f"{query} -is:retweet"

            app_logger.info(f"جاري البحث عن: {query}")

            # جلب التغريدات من API v2
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(count, 100),  # API limit per request
                tweet_fields=['created_at', 'public_metrics', 'lang', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )

            if not tweets.data:
                app_logger.warning("لم يتم العثور على تغريدات")
                return pd.DataFrame()

            # معالجة البيانات
            tweets_data = self._parse_tweets(tweets)

            app_logger.info(f"تم جلب {len(tweets_data)} تغريدة بنجاح")
            return tweets_data

        except tweepy.TweepyException as e:
            success, message = handle_api_error(e, "fetch_tweets")
            raise TwitterAPIError(message)
        except Exception as e:
            app_logger.error(f"خطأ غير متوقع: {str(e)}")
            raise TwitterAPIError(f"خطأ في جلب البيانات: {str(e)}")

    def _parse_tweets(self, tweets_response):
        """
        تحويل البيانات من API إلى DataFrame

        Args:
            tweets_response: استجابة API

        Returns:
            DataFrame: بيانات منظمة
        """
        tweets_list = []

        # إنشاء قاموس للمستخدمين
        users_dict = {}
        if tweets_response.includes and 'users' in tweets_response.includes:
            users_dict = {
                user.id: {
                    'username': user.username,
                    'name': user.name
                }
                for user in tweets_response.includes['users']
            }

        for tweet in tweets_response.data:
            # معلومات المستخدم
            user_info = users_dict.get(tweet.author_id, {
                'username': 'unknown',
                'name': 'Unknown'
            })

            # معلومات التفاعل
            metrics = tweet.public_metrics

            tweet_data = {
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'author_id': tweet.author_id,
                'username': user_info['username'],
                'user_name': user_info['name'],
                'likes': metrics.get('like_count', 0),
                'retweets': metrics.get('retweet_count', 0),
                'replies': metrics.get('reply_count', 0),
                'lang': tweet.lang if hasattr(tweet, 'lang') else 'unknown'
            }

            tweets_list.append(tweet_data)

        df = pd.DataFrame(tweets_list)

        # ترتيب حسب التاريخ (الأحدث أولاً)
        if not df.empty and 'created_at' in df.columns:
            df = df.sort_values('created_at', ascending=False).reset_index(drop=True)

        return df

    def fetch_by_keyword(self, keyword, count=100, lang='all'):
        """
        البحث بكلمة مفتاحية

        Args:
            keyword: الكلمة المفتاحية
            count: عدد التغريدات
            lang: اللغة

        Returns:
            DataFrame: التغريدات
        """
        return self.fetch_tweets(keyword, count, 'keyword', lang)

    def fetch_by_hashtag(self, hashtag, count=100, lang='all'):
        """
        البحث بهاشتاغ

        Args:
            hashtag: الهاشتاغ
            count: عدد التغريدات
            lang: اللغة

        Returns:
            DataFrame: التغريدات
        """
        return self.fetch_tweets(hashtag, count, 'hashtag', lang)

    def get_tweet_stats(self, df):
        """
        حساب إحصائيات التغريدات

        Args:
            df: DataFrame التغريدات

        Returns:
            dict: الإحصائيات
        """
        if df.empty:
            return {}

        stats = {
            'total_tweets': len(df),
            'total_likes': df['likes'].sum(),
            'total_retweets': df['retweets'].sum(),
            'avg_likes': df['likes'].mean(),
            'avg_retweets': df['retweets'].mean(),
            'most_liked': df.loc[df['likes'].idxmax()].to_dict() if len(df) > 0 else None,
            'most_retweeted': df.loc[df['retweets'].idxmax()].to_dict() if len(df) > 0 else None,
            'languages': df['lang'].value_counts().to_dict(),
            'date_range': {
                'from': df['created_at'].min(),
                'to': df['created_at'].max()
            }
        }

        return stats


# دالة مساعدة للاستخدام السريع
def quick_fetch(query, count=100, search_type='keyword', lang='all'):
    """
    دالة سريعة لجلب التغريدات

    Args:
        query: نص البحث
        count: عدد التغريدات
        search_type: نوع البحث
        lang: اللغة

    Returns:
        DataFrame: التغريدات
    """
    fetcher = TwitterDataFetcher()
    return fetcher.fetch_tweets(query, count, search_type, lang)
