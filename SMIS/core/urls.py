from django.urls import path
from . import views

urlpatterns = [
    # Teacher URLs
    path('teacher/courses/', views.TeacherCourseList.as_view(), name='teacher_courses'),
    path('teacher/course/<int:course_id>/assessment/', views.CreateAssessmentView.as_view(), name='create_assessment'),
    
    # HRT URLs
    path('hrt/student/<int:pk>/update/', views.HRTStudentUpdate.as_view(), name='hrt_student_update'),
    path('hrt/attendance/<int:student_id>/', views.AttendanceCreateView.as_view(), name='hrt_attendance'),
    
    # PDF Generation
    path('assessment/<int:assessment_id>/pdf/', views.generate_mark_list_pdf, name='generate_mark_list_pdf'),
]