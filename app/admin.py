
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)
# Register your models here.

admin.site.register(Course)
admin.site.register(Session_Year)

# Register Student Model
admin.site.register(Student)

admin.site.register(Staff)

admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Staff_leave)
admin.site.register(Staff_Feedback)
admin.site.register(Student_Notification)
admin.site.register(Student_Feedback)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
admin.site.register(StudentResult)


