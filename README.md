# Graph Search Visualizer 🌐

تطبيق ويب تفاعلي لتصور خوارزميات البحث في الرسوم البيانية

## المميزات ✨

- **واجهة ويب حديثة** باستخدام Streamlit
- **ثلاث خوارزميات بحث**:
  - 🔍 **DFS** (Depth-First Search)
  - 🔍 **BFS** (Breadth-First Search)
  - 🔄 **Bidirectional Search**
- **تصور متحرك** يظهر:
  - مسار الاستكشاف (العقد التي تم زيارتها)
  - مسار الحل النهائي (من البداية إلى الهدف)
- **ألوان مميزة**:
  - 🟠 برتقالي: نقطة البداية والنهاية
  - 🔵 أزرق فاتح: عقد غير مستكشفة
  - 🟢 أخضر فاتح: عقد تمت زيارتها
  - 🟡 ذهبي: العقدة الحالية
  - 🔴 أحمر: عقد مسار الحل

## التشغيل المحلي 💻

### 1. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل التطبيق
```bash
streamlit run app.py
```

سيتم فتح التطبيق في المتصفح على العنوان: `http://localhost:8501`

## النشر على Streamlit Cloud (مجاني) 🌐

### الخطوات:

1. **إنشاء حساب على GitHub**
   - اذهب إلى [GitHub.com](https://github.com)
   - أنشئ حساب جديد (مجاني)

2. **إنشاء مستودع جديد**
   - اضغط على "New repository"
   - أعطيه اسم مثل: `graph-search-visualizer`
   - اختر "Public" (للاستخدام المجاني)
   - اضغط "Create repository"

3. **رفع الملفات إلى GitHub**
   ```bash
   cd C:\Users\maysh\Desktop\graph_search_app
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/graph-search-visualizer.git
   git push -u origin main
   ```
   
   أو استخدم GitHub Desktop (أسهل)

4. **النشر على Streamlit Cloud**
   - اذهب إلى [share.streamlit.io](https://share.streamlit.io)
   - سجل دخول بحساب GitHub
   - اضغط "New app"
   - اختر المستودع: `graph-search-visualizer`
   - Main file path: `app.py`
   - اضغط "Deploy"

5. **الوصول للتطبيق**
   - ستحصل على رابط مثل: `https://your-app-name.streamlit.app`
   - يمكنك مشاركة هذا الرابط مع الدكتور! 🎉

## ملفات المشروع 📁

- `app.py` - التطبيق الرئيسي (Streamlit)
- `graph_search_visualizer.py` - النسخة الأصلية (للحاسوب)
- `requirements.txt` - المكتبات المطلوبة
- `README.md` - هذا الملف

## الاستخدام 📖

1. اختر خوارزمية البحث من الأزرار الجانبية
2. شاهد الرسم البياني يتحدث مع التقدم
3. راجع قائمة المسار المختبر على اليمين
4. اضغط "Reset" لإعادة التشغيل

## الدعم 💬

إذا واجهت أي مشاكل، تأكد من:
- تثبيت جميع المكتبات من `requirements.txt`
- استخدام Python 3.8 أو أحدث
- أن تكون متصل بالإنترنت عند النشر

---

**تم التطوير بـ ❤️ للاستخدام التعليمي**
