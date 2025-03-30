# core/urls.py
urlpatterns = [
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('hrt/', views.hrt_dashboard, name='hrt_dashboard'),
    # Add other role-specific URLs
]