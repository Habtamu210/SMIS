from django.contrib import admin
from .models import User, Student

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_active')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('idno', 'grade_level', 'section')