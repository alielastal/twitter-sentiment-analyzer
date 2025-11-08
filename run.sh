#!/bin/bash

# سكريبت لتشغيل تطبيق Twitter Sentiment Analyzer

echo "🚀 جاري تشغيل محلل مشاعر تويتر..."
echo ""

# التحقق من ملف .env
if [ ! -f .env ]; then
    echo "❌ خطأ: ملف .env غير موجود!"
    echo "الرجاء نسخ .env.example إلى .env وإضافة مفاتيح Twitter API"
    echo ""
    echo "قم بتشغيل:"
    echo "  cp .env.example .env"
    echo "  nano .env  # أو استخدم أي محرر نصوص"
    exit 1
fi

# البحث عن streamlit
if command -v streamlit &> /dev/null; then
    # streamlit موجود في PATH
    streamlit run app.py
elif [ -f ~/.local/bin/streamlit ]; then
    # استخدام المسار المحلي
    ~/.local/bin/streamlit run app.py
else
    echo "❌ خطأ: Streamlit غير مثبت!"
    echo "الرجاء تثبيته باستخدام:"
    echo "  pip3 install streamlit"
    exit 1
fi
