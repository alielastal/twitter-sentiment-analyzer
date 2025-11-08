"""
نظام إدارة الأخطاء
"""
from utils.logger import app_logger


class TwitterAPIError(Exception):
    """خطأ في الاتصال بـ Twitter API"""
    pass


class DataProcessingError(Exception):
    """خطأ في معالجة البيانات"""
    pass


class AnalysisError(Exception):
    """خطأ في تحليل المشاعر"""
    pass


def handle_api_error(error, context=""):
    """
    معالجة أخطاء API

    Args:
        error: كائن الخطأ
        context: سياق الخطأ

    Returns:
        tuple: (success: bool, message: str)
    """
    error_message = str(error)

    # التعامل مع أخطاء معينة
    if "429" in error_message or "rate limit" in error_message.lower():
        message = "⚠️ تم تجاوز حد الطلبات. الرجاء الانتظار 15 دقيقة."
        app_logger.warning(f"Rate limit exceeded: {context}")
        return False, message

    elif "401" in error_message or "unauthorized" in error_message.lower():
        message = "❌ خطأ في المصادقة. تحقق من مفاتيح API."
        app_logger.error(f"Authentication error: {context}")
        return False, message

    elif "404" in error_message:
        message = "❌ البيانات المطلوبة غير موجودة."
        app_logger.error(f"Not found error: {context}")
        return False, message

    elif "connection" in error_message.lower() or "timeout" in error_message.lower():
        message = "⚠️ خطأ في الاتصال بالإنترنت. تحقق من اتصالك."
        app_logger.error(f"Connection error: {context}")
        return False, message

    else:
        message = f"❌ حدث خطأ: {error_message}"
        app_logger.error(f"Unexpected error in {context}: {error_message}")
        return False, message


def handle_data_error(error, context=""):
    """
    معالجة أخطاء البيانات

    Args:
        error: كائن الخطأ
        context: سياق الخطأ

    Returns:
        tuple: (success: bool, message: str)
    """
    error_message = str(error)
    message = f"❌ خطأ في معالجة البيانات: {error_message}"
    app_logger.error(f"Data processing error in {context}: {error_message}")
    return False, message


def validate_input(query, tweet_count, min_count=50, max_count=1000):
    """
    التحقق من صحة المدخلات

    Args:
        query: نص البحث
        tweet_count: عدد التغريدات
        min_count: الحد الأدنى
        max_count: الحد الأقصى

    Returns:
        tuple: (valid: bool, message: str)
    """
    # التحقق من النص
    if not query or query.strip() == "":
        return False, "❌ الرجاء إدخال نص للبحث"

    if len(query.strip()) < 2:
        return False, "❌ النص المدخل قصير جداً (على الأقل حرفان)"

    # التحقق من عدد التغريدات
    if tweet_count < min_count:
        return False, f"❌ العدد أقل من الحد الأدنى ({min_count})"

    if tweet_count > max_count:
        return False, f"❌ العدد أكبر من الحد الأقصى ({max_count})"

    return True, "✅ المدخلات صحيحة"


def safe_execute(func, error_message="حدث خطأ أثناء التنفيذ", *args, **kwargs):
    """
    تنفيذ دالة بشكل آمن مع معالجة الأخطاء

    Args:
        func: الدالة المراد تنفيذها
        error_message: رسالة الخطأ
        *args, **kwargs: معاملات الدالة

    Returns:
        tuple: (success: bool, result: any, message: str)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, "نجح"
    except Exception as e:
        app_logger.error(f"Error in {func.__name__}: {str(e)}")
        return False, None, f"{error_message}: {str(e)}"
