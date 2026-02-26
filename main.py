from flet import *
import requests
import time

DB_URL = "FIREBASE_LIN"




def main(page: Page):
    page.scroll = 'auto'
    page.theme_mode = ThemeMode.LIGHT

    
    
    
    
    def get_students_count():
        response = requests.get(DB_URL)
        if response.status_code != 200:
            return 0

        data = response.json()

        if not data:
            return 0

        return len(data)


    



    # دالة عرض الرسالة (مع زر إغلاق)
    def show1(msg="تمت إضافة الطالب بنجاح ✅"):
        def close_dialog(e):
            alert1.open = False
            page.update()

        alert1 = AlertDialog(
            title=Text(msg, size=18, color=Colors.GREEN),
            actions=[TextButton("تم", on_click=close_dialog)],
            actions_alignment=MainAxisAlignment.END,
        )
        page.overlay.append(alert1)
        alert1.open = True
        page.update()
    
    def is_valid_mark(value):
        return value.isdigit() and 0 <= int(value) <= 100

    
    def show6(msg):
        def close_dialog(e):
            alert1.open = False
            page.update()
        alert1 = AlertDialog(
            title=Text(msg, size=14),
            actions=[TextButton("تم", on_click=close_dialog)],
            actions_alignment=MainAxisAlignment.END,
        )
        page.overlay.append(alert1)
        alert1.open = True
        page.update()
    
    count_text = Text(str(get_students_count()), size=18, font_family="IBM Plex Sans Arabic")
    def add(e):
        fields = [
            name.value,
            email.value,
            phone.value,
            address.value,
            maths.value,
            arabic.value,
            german.value,
            english.value,
            draw.value,
            chemistrt.value
        ]
        
        if any(field.strip() == "" for field in fields):
            def close_dialog(ev):
                alert.open = False
                page.update()
            alert = AlertDialog(
                title=Text("اكمل باقي المطلوب"),
                actions=[TextButton("تم", on_click=close_dialog)],
                actions_alignment=MainAxisAlignment.END,
            )
            page.overlay.append(alert)
            alert.open = True
            page.update()
            return
        
        marks = [
            maths.value,
            arabic.value,
            german.value,
            english.value,
            draw.value,
            chemistrt.value
        ]

        if not all(is_valid_mark(m) for m in marks):
            show6("الدرجات يجب أن تكون أرقام من 0 إلى 100")
            page.update()
            return
        def mon1():
            if not all(int(m) >= 50 for m in marks):
                show6("انت راسب")
                page.update()
                return
        
        def mon2():
            if not all(int(m) <= 50 for m in marks):
                show6("انت ناجح")
                page.update()
                return
        
        payload = {
            "name": name.value.capitalize(),
            "email": email.value,
            "phone": phone.value,
            "address": address.value,
            "math": maths.value,
            "arabic": arabic.value,
            "german": german.value,
            "english": english.value,
            "drawing": draw.value,
            "chemistry": chemistrt.value
        }

        try:
            r = requests.post(DB_URL, json=payload)
            if r.status_code != 200:
                raise Exception(f"Failed to save user. Status code: {r.status_code}")
            show6(f"{name.value.capitalize()} : تم اضافة الطالب")
            row_count = str(get_students_count())
            time.sleep(2)
            mon1()
            mon2()
            page.update()
        except Exception as ex:
            def close_dialog(ev):
                alert.open = False
                page.update()
            alert = AlertDialog(
                title=Text("Error saving data"),
                content=Text(str(ex)),
                actions=[TextButton("Ok", on_click=close_dialog)],
                actions_alignment=MainAxisAlignment.END,
            )
            page.overlay.append(alert)
            alert.open = True
            page.update()
            return


    def show2(e):
        response = requests.get(DB_URL)

        if response.status_code != 200:
            show1("فشل الاتصال بقاعدة البيانات ❌")
            return

        data = response.json()

        if not data:
            show1("لا يوجد طلاب حالياً ❌")
            return

        page.clean()

        # عنوان الصفحة
        page.add(
            Row(
                [Text("قائمة الطلاب المسجلين", size=20, weight="bold", color=Colors.BLUE)],
                alignment=MainAxisAlignment.CENTER
            )
        )

        # Firebase بيرجع Dictionary
        for key, student in data.items():
            card = Card(
                elevation=3,
                content=Container(
                    padding=10,
                    bgcolor=Colors.BLUE_100,
                    border_radius=10,
                    content=Column([
                        Text(f"📘 الاسم: {student.get('name','')}", size=16, weight="bold"),
                        Text(f"📧 البريد: {student.get('email','')}"),
                        Text(f"📱 الهاتف: {student.get('phone','')}"),
                        Text(f"🏠 العنوان: {student.get('address','')}"),
                        Divider(),
                        Text(f"📊 الرياضيات: {student.get('math','')} | العربي: {student.get('arabic','')}"),
                        Text(f"🌍 الألماني: {student.get('german','')} | الإنجليزي: {student.get('english','')}"),
                        Text(f"🎨 الرسم: {student.get('drawing','')} | 🧪 الكيمياء: {student.get('chemistry','')}")
                    ])
                )
            )

            page.add(card)



        # 🔙 زر الرجوع إلى الشاشة الرئيسية
        def go_back(e):
            page.clean()  # يمسح شاشة العرض
            main(page)    # يعيد تحميل الواجهة الأصلية (إضافة الطالب)

        page.add(
            Row([
                ElevatedButton("🔙 الرجوع", on_click=go_back, style=ButtonStyle(bgcolor='red', color='white'))
            ], alignment=MainAxisAlignment.CENTER)
        )

        page.update()

    # الحقول
    name = TextField(label="اسم الطالب", icon=Icons.PERSON, rtl=True)
    email = TextField(label="البريد الالكتروني", icon=Icons.EMAIL, rtl=True)
    phone = TextField(label="هاتف الطالب", icon=Icons.PHONE, rtl=True)
    address = TextField(label="العنوان او السكن", icon=Icons.LOCATION_CITY, rtl=True)

    # العلامات
    mark1 = Text("علامات الطالب", text_align='center', width=390, size=17)
    maths = TextField(label="رياضيات", width=110, rtl=True, keyboard_type=KeyboardType.NUMBER)
    arabic = TextField(label="عربي", width=110, rtl=True, keyboard_type=KeyboardType.NUMBER)
    german = TextField(label="الماني", width=110, rtl=True, keyboard_type=KeyboardType.NUMBER)
    english = TextField(label="انجليزية", width=110, rtl=True, keyboard_type=KeyboardType.NUMBER)
    draw = TextField(label="الرسم", width=110, rtl=True, keyboard_type=KeyboardType.NUMBER)
    chemistrt = TextField(label="كيمياء", width=110, rtl=True, keyboard_type=KeyboardType.NUMBER)
    
    
    
    # الأزرار
    bt1 = ElevatedButton(
        "إضافة طالب جديد",
        width=170,
        style=ButtonStyle(bgcolor='blue', color='white', padding=15),
        on_click=add
    )

    bt2 = ElevatedButton(
        "عرض كل الطلاب",
        width=170,
        style=ButtonStyle(bgcolor='blue', color='white', padding=15),
        on_click=show2  # ← هنا كان غلط كنت كاتب lambda _: show2
    )

    row1 = Row([Image(src="home.gif")], alignment=MainAxisAlignment.CENTER)
    row2 = Row([Text("تطبيق الطالب و المعلم في جيبك", size=18, font_family="IBM Plex Sans Arabic")],
               alignment=MainAxisAlignment.CENTER)
    row3 = Row([
        Text("عدد الطلاب المسجلين : ", size=18, font_family="IBM Plex Sans Arabic", color=Colors.BLUE),
        count_text
    ], alignment=MainAxisAlignment.CENTER, rtl=True)

    page.add(
        row1, row2, row3,
        name, email, phone, address,
        mark1,
        Row([maths, arabic, german], alignment=MainAxisAlignment.CENTER, rtl=True),
        Row([english, draw, chemistrt], alignment=MainAxisAlignment.CENTER, rtl=True),
        Row([bt1, bt2], alignment=MainAxisAlignment.CENTER, rtl=True)
    )

    page.update()


app(main)
