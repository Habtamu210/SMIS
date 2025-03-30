from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, Assessment, Mark
from django.views.generic import UpdateView
from .models import Student, Attendance

class TeacherCourseList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = 'teacher/course_list.html'

    def test_func(self):
        return self.request.user.role == 'TEACHER'

    def get_queryset(self):
        return Course.objects.filter(teachers__user=self.request.user)

class CreateAssessmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assessment
    fields = ['name', 'weight', 'max_score']
    template_name = 'teacher/create_assessment.html'

    def test_func(self):
        return self.request.user.role == 'TEACHER'

    def form_valid(self, form):
        form.instance.course = Course.objects.get(id=self.kwargs['course_id'])
        return super().form_valid(form)

class MarkEntryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mark
    fields = ['score']
    template_name = 'teacher/mark_entry.html'

    def test_func(self):
        return self.request.user.role == 'TEACHER'
    

class HRTStudentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    fields = ['idno', 'birth_date', 'grade_level']
    template_name = 'hrt/student_update.html'

    def test_func(self):
        return self.request.user.role == 'HRT'

class AttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Attendance
    fields = ['date', 'status']
    template_name = 'hrt/attendance_create.html'

    def test_func(self):
        return self.request.user.role == 'HRT'

    def form_valid(self, form):
        form.instance.student = Student.objects.get(id=self.kwargs['student_id'])
        form.instance.recorded_by = self.request.user.staff_profile
        return super().form_valid(form)