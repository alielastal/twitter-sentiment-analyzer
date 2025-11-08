"""
تحليل المشاعر باستخدام TextBlob و VADER
"""
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config.settings import POSITIVE_THRESHOLD, NEGATIVE_THRESHOLD
from utils.logger import app_logger
from src.text_cleaner import TextCleaner


class SentimentAnalyzer:
    """فئة لتحليل المشاعر"""

    def __init__(self):
        """تهيئة المحلل"""
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.text_cleaner = TextCleaner()

    def analyze_with_textblob(self, text):
        """
        تحليل المشاعر باستخدام TextBlob

        Args:
            text: النص المراد تحليله

        Returns:
            dict: نتيجة التحليل
        """
        if not text or text.strip() == "":
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'محايد'
            }

        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            # تصنيف المشاعر
            if polarity > POSITIVE_THRESHOLD:
                sentiment = 'إيجابي'
            elif polarity < NEGATIVE_THRESHOLD:
                sentiment = 'سلبي'
            else:
                sentiment = 'محايد'

            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment': sentiment
            }

        except Exception as e:
            app_logger.error(f"خطأ في تحليل TextBlob: {str(e)}")
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'محايد'
            }

    def analyze_with_vader(self, text):
        """
        تحليل المشاعر باستخدام VADER

        Args:
            text: النص المراد تحليله

        Returns:
            dict: نتيجة التحليل
        """
        if not text or text.strip() == "":
            return {
                'compound': 0.0,
                'pos': 0.0,
                'neu': 0.0,
                'neg': 0.0,
                'sentiment': 'محايد'
            }

        try:
            scores = self.vader_analyzer.polarity_scores(text)
            compound = scores['compound']

            # تصنيف المشاعر بناءً على compound score
            if compound >= 0.05:
                sentiment = 'إيجابي'
            elif compound <= -0.05:
                sentiment = 'سلبي'
            else:
                sentiment = 'محايد'

            return {
                'compound': round(compound, 3),
                'pos': round(scores['pos'], 3),
                'neu': round(scores['neu'], 3),
                'neg': round(scores['neg'], 3),
                'sentiment': sentiment
            }

        except Exception as e:
            app_logger.error(f"خطأ في تحليل VADER: {str(e)}")
            return {
                'compound': 0.0,
                'pos': 0.0,
                'neu': 0.0,
                'neg': 0.0,
                'sentiment': 'محايد'
            }

    def analyze_dataframe(self, df, text_column='cleaned_text', method='textblob'):
        """
        تحليل مشاعر DataFrame كامل

        Args:
            df: DataFrame يحتوي على النصوص
            text_column: اسم عمود النصوص
            method: طريقة التحليل ('textblob', 'vader', 'both')

        Returns:
            DataFrame: مع أعمدة نتائج التحليل
        """
        if df.empty:
            app_logger.warning("DataFrame فارغ")
            return df

        app_logger.info(f"جاري تحليل {len(df)} نص باستخدام {method}...")

        results = []

        for idx, row in df.iterrows():
            text = row.get(text_column, "")

            result = {'index': idx}

            if method == 'textblob':
                analysis = self.analyze_with_textblob(text)
                result['polarity'] = analysis['polarity']
                result['subjectivity'] = analysis['subjectivity']
                result['sentiment'] = analysis['sentiment']

            elif method == 'vader':
                analysis = self.analyze_with_vader(text)
                result['compound'] = analysis['compound']
                result['pos_score'] = analysis['pos']
                result['neu_score'] = analysis['neu']
                result['neg_score'] = analysis['neg']
                result['sentiment'] = analysis['sentiment']

            elif method == 'both':
                # استخدام كلا الطريقتين
                tb_analysis = self.analyze_with_textblob(text)
                vader_analysis = self.analyze_with_vader(text)

                result['tb_polarity'] = tb_analysis['polarity']
                result['tb_subjectivity'] = tb_analysis['subjectivity']
                result['vader_compound'] = vader_analysis['compound']

                # تحديد المشاعر النهائية بناءً على كلا التحليلين
                avg_score = (tb_analysis['polarity'] + vader_analysis['compound']) / 2
                if avg_score > 0.05:
                    result['sentiment'] = 'إيجابي'
                elif avg_score < -0.05:
                    result['sentiment'] = 'سلبي'
                else:
                    result['sentiment'] = 'محايد'

            results.append(result)

        # دمج النتائج مع DataFrame الأصلي
        results_df = pd.DataFrame(results)
        df = df.merge(results_df.drop('index', axis=1), left_index=True, right_index=True, how='left')

        app_logger.info("اكتمل التحليل بنجاح")
        return df

    def get_sentiment_statistics(self, df, sentiment_column='sentiment'):
        """
        حساب إحصائيات المشاعر

        Args:
            df: DataFrame مع نتائج التحليل
            sentiment_column: اسم عمود المشاعر

        Returns:
            dict: الإحصائيات
        """
        if df.empty or sentiment_column not in df.columns:
            return {}

        total = len(df)
        sentiment_counts = df[sentiment_column].value_counts()

        stats = {
            'total': total,
            'positive': sentiment_counts.get('إيجابي', 0),
            'negative': sentiment_counts.get('سلبي', 0),
            'neutral': sentiment_counts.get('محايد', 0),
            'positive_pct': round((sentiment_counts.get('إيجابي', 0) / total) * 100, 2),
            'negative_pct': round((sentiment_counts.get('سلبي', 0) / total) * 100, 2),
            'neutral_pct': round((sentiment_counts.get('محايد', 0) / total) * 100, 2)
        }

        # حساب المتوسطات إذا كانت الأعمدة موجودة
        if 'polarity' in df.columns:
            stats['avg_polarity'] = round(df['polarity'].mean(), 3)

        if 'compound' in df.columns:
            stats['avg_compound'] = round(df['compound'].mean(), 3)

        return stats

    def get_extreme_sentiments(self, df, n=5):
        """
        الحصول على أكثر التغريدات إيجابية وسلبية

        Args:
            df: DataFrame مع نتائج التحليل
            n: عدد التغريدات لكل فئة

        Returns:
            dict: أكثر التغريدات تطرفاً
        """
        result = {
            'most_positive': pd.DataFrame(),
            'most_negative': pd.DataFrame()
        }

        if df.empty:
            return result

        # تحديد العمود المستخدم للترتيب
        if 'polarity' in df.columns:
            score_col = 'polarity'
        elif 'compound' in df.columns:
            score_col = 'compound'
        else:
            return result

        # أكثر التغريدات إيجابية
        positive_df = df[df['sentiment'] == 'إيجابي'].nlargest(n, score_col)
        result['most_positive'] = positive_df

        # أكثر التغريدات سلبية
        negative_df = df[df['sentiment'] == 'سلبي'].nsmallest(n, score_col)
        result['most_negative'] = negative_df

        return result

    def analyze_sentiment_over_time(self, df, time_column='created_at', sentiment_column='sentiment'):
        """
        تحليل تطور المشاعر عبر الزمن

        Args:
            df: DataFrame مع التواريخ والمشاعر
            time_column: عمود التاريخ
            sentiment_column: عمود المشاعر

        Returns:
            DataFrame: التوزيع الزمني للمشاعر
        """
        if df.empty or time_column not in df.columns or sentiment_column not in df.columns:
            return pd.DataFrame()

        # التأكد من أن العمود من نوع datetime
        if not pd.api.types.is_datetime64_any_dtype(df[time_column]):
            df[time_column] = pd.to_datetime(df[time_column])

        # تجميع حسب الساعة والمشاعر
        df['hour'] = df[time_column].dt.floor('H')

        time_sentiment = df.groupby(['hour', sentiment_column]).size().unstack(fill_value=0)

        # حساب النسب
        time_sentiment_pct = time_sentiment.div(time_sentiment.sum(axis=1), axis=0) * 100

        return time_sentiment_pct


# دوال مساعدة للاستخدام السريع
def quick_analyze(text, method='textblob'):
    """
    تحليل سريع لنص واحد

    Args:
        text: النص
        method: طريقة التحليل

    Returns:
        dict: نتيجة التحليل
    """
    analyzer = SentimentAnalyzer()

    if method == 'textblob':
        return analyzer.analyze_with_textblob(text)
    elif method == 'vader':
        return analyzer.analyze_with_vader(text)
    else:
        return analyzer.analyze_with_textblob(text)


def quick_analyze_dataframe(df, text_column='cleaned_text', method='textblob'):
    """
    تحليل سريع لـ DataFrame

    Args:
        df: DataFrame
        text_column: عمود النصوص
        method: طريقة التحليل

    Returns:
        DataFrame: مع نتائج التحليل
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_dataframe(df, text_column, method)
