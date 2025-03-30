from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test

def is_teacher(user):
    return user.role == 'TEACHER'

@login_required
@user_passes_test(is_teacher)
def create_assessment(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        # Process form to create assessment
    return render(request, 'teacher/create_assessment.html', {'course': course})