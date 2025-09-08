# (empty)

from PyQt6.QtCore import QObject, pyqtSignal

class Translator(QObject):
	language_changed = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self._language = "English"
		self._translations = {
			"English": {
				"Dashboard": "Dashboard",
				"Employees": "Employees",
				"Analytics": "Analytics",
				"Settings": "Settings",
				"Add Employee": "Add Employee",
				"Edit": "Edit",
				"Delete": "Delete",
				"Export CSV": "Export CSV",
				"Import CSV": "Import CSV",
				"Search": "Search:",
				"Salary": "Salary:",
				"DOB": "DOB:",
				"Language": "Language:",
				"Toggle Theme": "Toggle Theme",
				"Change Logo": "Change Logo",
				"Backup Data": "Backup Data",
				"Restore Data": "Restore Data",
				"Total Employees": "Total Employees: <b>{count}</b>",
				"No Data": "No employees to export.",
				"Export Complete": "Export Complete",
				"Import Complete": "Import Complete",
				"Backup Complete": "Backup Complete",
				"Restore Complete": "Restore Complete",
				"Language Changed": "Language Changed",
				"Language set to": "Language set to {lang}.",
				"First Name": "First Name",
				"Last Name": "Last Name",
				"Date of Birth": "Date of Birth",
				"Emirates ID": "Emirates ID",
				"Passport Number": "Passport Number",
				"EID Front": "Emirates ID Front",
				"EID Back": "Emirates ID Back",
				"Passport Image": "Passport Image",
				"Actions": "Actions",
				"Select Emirates ID Front": "Select Emirates ID Front",
				"Select Emirates ID Back": "Select Emirates ID Back",
				"Select Passport Image": "Select Passport Image",
				"Add / Edit Employee": "Add / Edit Employee",
				"Error": "Error",
				"First and Last name are required!": "First and Last name are required!",
				"Backup Database": "Backup Database",
				"Restore Database": "Restore Database",
				"DB Files (*.db)": "DB Files (*.db)",
				"Images (*.png *.jpg *.bmp)": "Images (*.png *.jpg *.bmp)",
				"Images (*.png *.jpg *.jpeg)": "Images (*.png *.jpg *.jpeg)",
				"Select Logo": "Select Logo",
				"Select Image": "Select Image",
				"All": "All",
				"All Years": "All Years",
				"Before 1990": "Before 1990",
				"1990-2000": "1990-2000",
				"After 2000": "After 2000",
				"< 5000": "< 5000",
				"> 10000": "> 10000",
				"5000-10000": "5000-10000",
			},
			"Arabic": {
				"Dashboard": "لوحة القيادة",
				"Employees": "الموظفون",
				"Analytics": "تحليلات",
				"Settings": "الإعدادات",
				"Add Employee": "إضافة موظف",
				"Edit": "تعديل",
				"Delete": "حذف",
				"Export CSV": "تصدير CSV",
				"Import CSV": "استيراد CSV",
				"Search": "بحث:",
				"Salary": "الراتب:",
				"DOB": "تاريخ الميلاد:",
				"Language": "اللغة:",
				"Toggle Theme": "تبديل النمط",
				"Change Logo": "تغيير الشعار",
				"Backup Data": "نسخ احتياطي للبيانات",
				"Restore Data": "استعادة البيانات",
				"Total Employees": "إجمالي الموظفين: <b>{count}</b>",
				"No Data": "لا يوجد موظفون للتصدير.",
				"Export Complete": "اكتمل التصدير",
				"Import Complete": "اكتمل الاستيراد",
				"Backup Complete": "اكتمل النسخ الاحتياطي",
				"Restore Complete": "اكتملت الاستعادة",
				"Language Changed": "تم تغيير اللغة",
				"Language set to": "تم تعيين اللغة إلى {lang}.",
				"First Name": "الاسم الأول",
				"Last Name": "اسم العائلة",
				"Date of Birth": "تاريخ الميلاد",
				"Emirates ID": "الهوية الإماراتية",
				"Passport Number": "رقم الجواز",
				"EID Front": "الهوية (أمامي)",
				"EID Back": "الهوية (خلفي)",
				"Passport Image": "صورة الجواز",
				"Actions": "إجراءات",
				"Select Emirates ID Front": "اختر الهوية (أمامي)",
				"Select Emirates ID Back": "اختر الهوية (خلفي)",
				"Select Passport Image": "اختر صورة الجواز",
				"Add / Edit Employee": "إضافة / تعديل موظف",
				"Error": "خطأ",
				"First and Last name are required!": "الاسم الأول واسم العائلة مطلوبان!",
				"Backup Database": "نسخ قاعدة البيانات احتياطيًا",
				"Restore Database": "استعادة قاعدة البيانات",
				"DB Files (*.db)": "ملفات قاعدة البيانات (*.db)",
				"Images (*.png *.jpg *.bmp)": "صور (*.png *.jpg *.bmp)",
				"Images (*.png *.jpg *.jpeg)": "صور (*.png *.jpg *.jpeg)",
				"Select Logo": "اختر الشعار",
				"Select Image": "اختر صورة",
				"All": "الكل",
				"All Years": "كل السنوات",
				"Before 1990": "قبل 1990",
				"1990-2000": "1990-2000",
				"After 2000": "بعد 2000",
				"< 5000": "< 5000",
				"> 10000": "> 10000",
				"5000-10000": "5000-10000",
			}
		}

	def set_language(self, language):
		if language != self._language:
			self._language = language
			self.language_changed.emit(language)

	def get_language(self):
		return self._language

	def tr(self, key, **kwargs):
		lang = self._language
		text = self._translations.get(lang, {}).get(key, key)
		if kwargs:
			return text.format(**kwargs)
		return text

translator = Translator()
