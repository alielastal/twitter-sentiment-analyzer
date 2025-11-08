"""
نظام السجلات للتطبيق
"""
import logging
import os
from datetime import datetime

def setup_logger(name='twitter_sentiment', level=logging.INFO):
    """
    إعداد نظام السجلات

    Args:
        name: اسم Logger
        level: مستوى السجلات (INFO, DEBUG, WARNING, ERROR)

    Returns:
        logger: كائن Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # تجنب إضافة handlers متعددة
    if logger.handlers:
        return logger

    # إنشاء مجلد logs إذا لم يكن موجوداً
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Handler للملف
    log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(level)

    # Handler للـ console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # تنسيق الرسائل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# إنشاء logger عام للتطبيق
app_logger = setup_logger()
