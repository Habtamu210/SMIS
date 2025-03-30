from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('HRT', 'Home Room Teacher'),
        ('HOD', 'Department Head'),
        ('COORDINATOR', 'Coordinator'),
        ('PRINCIPAL', 'Principal/Director'),
        ('PARENT', 'Parent'),
        ('RECORD_OFFICER', 'Record Officer'),
        ('ADMIN', 'System Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    idno = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    grade_level = models.IntegerField()
    section = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return self.user.get_full_name()

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField(Student, related_name='parents')
    relationship = models.CharField(max_length=20)  # Father/Mother/Guardian

    def __str__(self):
        return self.user.get_full_name()
    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Staff, through='TeacherAssignment')

    def __str__(self):
        return f"{self.code}: {self.title}"

class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 30.00%
    max_score = models.IntegerField()

    def save(self, *args, **kwargs):
        # Ensure total weight <= 100%
        total_weight = Assessment.objects.filter(course=self.course).aggregate(Sum('weight'))['weight__sum'] or 0
        if total_weight + self.weight > 100:
            raise ValidationError("Total assessment weight exceeds 100%")
        super().save(*args, **kwargs)

class Mark(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

class Class(models.Model):
    section_no = models.CharField(max_length=10)
    room_no = models.CharField(max_length=10)
    building_no = models.CharField(max_length=10)
    hrt = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='managed_classes')

class Department(models.Model):
    dno = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    hod = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='managed_department')

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Class, on_delete=models.CASCADE)

class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    generated_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    generation_date = models.DateField(auto_now_add=True)

