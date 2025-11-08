# 🔧 دليل التثبيت الكامل

## حل مشكلة "streamlit: command not found"

### السبب:
مسار `~/.local/bin` غير موجود في متغير البيئة `PATH`

---

## ✅ الحلول المتاحة:

### **الحل 1: استخدام السكريبت الجاهز (الأسهل)**

```bash
# على Linux/Mac
./run.sh

# على Windows
run.bat
```

---

### **الحل 2: إضافة المسار إلى PATH (حل دائم)**

#### على Linux/Mac:

```bash
# إضافة المسار إلى ملف .bashrc أو .zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# تفعيل التغييرات
source ~/.bashrc

# الآن يمكنك استخدام:
streamlit run app.py
```

---

### **الحل 3: استخدام المسار الكامل**

```bash
~/.local/bin/streamlit run app.py
```

---

### **الحل 4: استخدام Python module**

```bash
python3 -m streamlit run app.py
```

---

## 🚀 خطوات التشغيل الكاملة

### 1. التثبيت:
```bash
cd /home/pc/Documents/Claude\ Apps/twitter-sentiment-analyzer
pip3 install -r requirements.txt
```

### 2. إعداد المفاتيح:
```bash
cp .env.example .env
nano .env  # أضف مفاتيح Twitter API
```

### 3. التشغيل:
اختر إحدى الطرق التالية:

**أ. السكريبت (موصى به)**
```bash
./run.sh
```

**ب. مع إصلاح PATH**
```bash
# أولاً: أضف المسار إلى PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# ثم شغل التطبيق
streamlit run app.py
```

**ج. المسار الكامل**
```bash
~/.local/bin/streamlit run app.py
```

**د. عبر Python**
```bash
python3 -m streamlit run app.py
```

---

## 🌐 الوصول للتطبيق

بعد التشغيل، افتح المتصفح على:
- **Local URL**: http://localhost:8501
- **Network URL**: http://10.10.10.60:8501

---

## ❓ استكشاف المشاكل

### المشكلة: "ModuleNotFoundError: No module named 'streamlit'"
**الحل:**
```bash
pip3 install streamlit --upgrade
```

### المشكلة: "Permission denied: './run.sh'"
**الحل:**
```bash
chmod +x run.sh
```

### المشكلة: التطبيق لا يفتح في المتصفح
**الحل:**
افتح المتصفح يدوياً على: http://localhost:8501

### المشكلة: "Address already in use"
**الحل:**
```bash
# أوقف العملية الحالية
pkill -f streamlit

# أو استخدم منفذ آخر
streamlit run app.py --server.port 8502
```

---

## 📝 ملاحظات

1. **للاستخدام اليومي**: استخدم السكريبت `./run.sh`
2. **لحل دائم**: أضف `~/.local/bin` إلى PATH
3. **تحديث المكتبات**: `pip3 install -r requirements.txt --upgrade`
4. **إيقاف التطبيق**: اضغط `Ctrl+C` في Terminal

---

## 🎯 التحقق من التثبيت

```bash
# التحقق من Python
python3 --version

# التحقق من pip
pip3 --version

# التحقق من Streamlit
python3 -m streamlit --version

# قائمة المكتبات المثبتة
pip3 list | grep -E "streamlit|tweepy|plotly|pandas"
```

---

## ✅ كل شيء يعمل؟

إذا رأيت هذه الرسالة:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://10.10.10.60:8501
```

🎉 **تهانينا! التطبيق يعمل بنجاح!**

افتح المتصفح وابدأ التحليل!
