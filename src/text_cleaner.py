"""
تنظيف ومعالجة النصوص
"""
import re
import pandas as pd
from config.settings import (
    REMOVE_URLS, REMOVE_MENTIONS, REMOVE_HASHTAGS,
    REMOVE_SPECIAL_CHARS, ARABIC_STOP_WORDS
)
from utils.logger import app_logger


class TextCleaner:
    """فئة لتنظيف النصوص"""

    def __init__(self):
        """تهيئة المنظف"""
        self.arabic_stop_words = set(ARABIC_STOP_WORDS)

        # Stop words إنجليزية أساسية
        self.english_stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their'
        }

    def clean_text(self, text, remove_urls=REMOVE_URLS, remove_mentions=REMOVE_MENTIONS,
                   remove_hashtags=REMOVE_HASHTAGS, remove_special=REMOVE_SPECIAL_CHARS):
        """
        تنظيف نص واحد

        Args:
            text: النص المراد تنظيفه
            remove_urls: إزالة الروابط
            remove_mentions: إزالة الـ mentions
            remove_hashtags: إزالة الهاشتاغات
            remove_special: إزالة الرموز الخاصة

        Returns:
            str: النص المنظف
        """
        if not isinstance(text, str):
            return ""

        # إزالة الروابط
        if remove_urls:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # إزالة mentions (@username)
        if remove_mentions:
            text = re.sub(r'@\w+', '', text)

        # إزالة hashtags (# فقط أو الكلمة كلها)
        if remove_hashtags:
            text = re.sub(r'#\w+', '', text)
        else:
            # إزالة # فقط وترك الكلمة
            text = re.sub(r'#', '', text)

        # إزالة الرموز الخاصة (لكن نحتفظ بالأحرف العربية والإنجليزية)
        if remove_special:
            # نحتفظ بالأحرف العربية والإنجليزية والأرقام والمسافات
            text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)

        # توحيد الأحرف العربية
        text = self._normalize_arabic(text)

        # تنظيف المسافات الزائدة
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def _normalize_arabic(self, text):
        """
        توحيد الأحرف العربية

        Args:
            text: النص

        Returns:
            str: النص الموحد
        """
        # توحيد الألف
        text = re.sub(r'[إأآا]', 'ا', text)

        # توحيد الهاء
        text = re.sub(r'ة', 'ه', text)

        # توحيد الياء
        text = re.sub(r'ى', 'ي', text)

        # إزالة التشكيل
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

        return text

    def clean_dataframe(self, df, text_column='text'):
        """
        تنظيف عمود النصوص في DataFrame

        Args:
            df: DataFrame
            text_column: اسم العمود المحتوي على النصوص

        Returns:
            DataFrame: مع عمود جديد 'cleaned_text'
        """
        if df.empty:
            return df

        app_logger.info(f"جاري تنظيف {len(df)} نص...")

        # إنشاء عمود جديد للنصوص المنظفة
        df['cleaned_text'] = df[text_column].apply(self.clean_text)

        # إزالة النصوص الفارغة بعد التنظيف
        original_count = len(df)
        df = df[df['cleaned_text'].str.strip() != ''].reset_index(drop=True)

        removed_count = original_count - len(df)
        if removed_count > 0:
            app_logger.info(f"تم إزالة {removed_count} نص فارغ بعد التنظيف")

        app_logger.info("اكتمل التنظيف بنجاح")
        return df

    def detect_language(self, text):
        """
        كشف لغة النص (عربي أو إنجليزي)

        Args:
            text: النص

        Returns:
            str: 'ar' أو 'en' أو 'unknown'
        """
        if not text:
            return 'unknown'

        # حساب نسبة الأحرف العربية
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = arabic_chars + english_chars

        if total_chars == 0:
            return 'unknown'

        arabic_ratio = arabic_chars / total_chars

        if arabic_ratio > 0.5:
            return 'ar'
        elif arabic_ratio < 0.3:
            return 'en'
        else:
            return 'mixed'

    def remove_stop_words(self, text, lang='ar'):
        """
        إزالة stop words

        Args:
            text: النص
            lang: اللغة ('ar' أو 'en')

        Returns:
            str: النص بدون stop words
        """
        if not text:
            return ""

        words = text.split()

        if lang == 'ar':
            stop_words = self.arabic_stop_words
        elif lang == 'en':
            stop_words = self.english_stop_words
        else:
            stop_words = self.arabic_stop_words.union(self.english_stop_words)

        # تصفية الكلمات
        filtered_words = [word for word in words if word.lower() not in stop_words]

        return ' '.join(filtered_words)

    def extract_keywords(self, text, min_length=3):
        """
        استخراج الكلمات المفتاحية

        Args:
            text: النص
            min_length: الحد الأدنى لطول الكلمة

        Returns:
            list: قائمة الكلمات المفتاحية
        """
        if not text:
            return []

        # تنظيف النص
        cleaned = self.clean_text(text)

        # كشف اللغة
        lang = self.detect_language(cleaned)

        # إزالة stop words
        without_stops = self.remove_stop_words(cleaned, lang)

        # استخراج الكلمات
        words = without_stops.split()

        # تصفية الكلمات القصيرة
        keywords = [word for word in words if len(word) >= min_length]

        return keywords

    def get_word_frequency(self, df, text_column='cleaned_text', top_n=20):
        """
        حساب تكرار الكلمات

        Args:
            df: DataFrame
            text_column: عمود النصوص
            top_n: عدد أكثر الكلمات تكراراً

        Returns:
            DataFrame: الكلمات وتكرارها
        """
        if df.empty or text_column not in df.columns:
            return pd.DataFrame()

        all_words = []

        for text in df[text_column]:
            keywords = self.extract_keywords(text)
            all_words.extend(keywords)

        # حساب التكرار
        word_freq = pd.Series(all_words).value_counts().head(top_n)

        result_df = pd.DataFrame({
            'word': word_freq.index,
            'frequency': word_freq.values
        })

        return result_df


# دوال مساعدة للاستخدام السريع
def quick_clean(text):
    """
    تنظيف سريع لنص واحد

    Args:
        text: النص

    Returns:
        str: النص المنظف
    """
    cleaner = TextCleaner()
    return cleaner.clean_text(text)


def quick_clean_dataframe(df, text_column='text'):
    """
    تنظيف سريع لـ DataFrame

    Args:
        df: DataFrame
        text_column: عمود النصوص

    Returns:
        DataFrame: مع النصوص المنظفة
    """
    cleaner = TextCleaner()
    return cleaner.clean_dataframe(df, text_column)
