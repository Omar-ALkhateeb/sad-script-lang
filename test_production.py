try:
    from edu.stdlib import *
except ImportError:
    from stdlib import *
الطلاب = ["أحمد", "سارة", "علي", "نور"]  #__EDU_LINE__:2
if ("سارة" in الطلاب):  #__EDU_LINE__:4
    edu_print("✅ سارة مسجلة في القائمة!")  #__EDU_LINE__:5
النقاط_الكلية = 0  #__EDU_LINE__:9
def اضف_مكافأة(قيمة):  #__EDU_LINE__:11
    global النقاط_الكلية
    النقاط_الكلية += حساب_المضاعف(قيمة)  #__EDU_LINE__:12
def حساب_المضاعف(س):  #__EDU_LINE__:15
    return (س * 2)  #__EDU_LINE__:16
اضف_مكافأة(15)  #__EDU_LINE__:19
edu_print(edu_add("النقاط الكلية بعد المكافأة: ", النقاط_الكلية))  #__EDU_LINE__:20
بيانات = {"الاسم": ["أحمد", "سارة", "علي", "نور"], "الدرجة": [88, 96, 75, 92]}  #__EDU_LINE__:23
جدول = باندا.DataFrame(بيانات)  #__EDU_LINE__:27
افضل_طالبين = جدول.sort_values(by="الدرجة", ascending=False).head(2)  #__EDU_LINE__:28
edu_print("\n=== أفضل طالبين ===")  #__EDU_LINE__:29
edu_print(افضل_طالبين)  #__EDU_LINE__:30
try:  #__EDU_LINE__:33
    نتيجة = (10 / 0)  #__EDU_LINE__:34
except EduInfiniteLoopError:
    raise
except Exception as خطأ_قسمة:
    edu_print("\nتم الإمساك بالخطأ بأمان داخل بلوك (حاول/التقط)!")  #__EDU_LINE__:36
جدول.ارسم_أعمدة("الاسم", "الدرجة", title="درجات الطلاب")  #__EDU_LINE__:40