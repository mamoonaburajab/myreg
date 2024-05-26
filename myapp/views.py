# File: myapp/views.py
from django.contrib.auth.decorators import login_required
from .models import Course, StudentRegistration
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Course, Student, StudentRegistration
                
from .models import Course
def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        # Validation checks
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already used')
            return render(request, 'register.html')
        
        # User creation
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        auth_login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('home')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('course_list')
        else:
            messages.error(request, 'Invalid login credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def course_list(request):
    courses = Course.objects.all()
   
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def register_course(request, course_id):
    user_id = request.user.id
    course = get_object_or_404(Course, id=course_id)

    if course.capacity > 0:
        registration, created = StudentRegistration.objects.get_or_create(
            user_id=user_id,  # Changed from student to user_id
            course=course
        )
        if created:
            course.capacity -= 1
            course.save()
            messages.success(request, "You have successfully registered for the course.")
        else:
            messages.info(request, "You are already registered for this course.")
    else:
        messages.error(request, "This course is full.")
    return redirect('course_list')
    

def course_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        courses = Course.objects.filter(
            Q(name__icontains=search_query) | 
            Q(code__icontains=search_query) | 
            Q(instructor__icontains=search_query)
        ).select_related('schedule')
    else:
        courses = Course.objects.all().select_related('schedule')
    return render(request, 'course_list.html', {'courses': courses})
def registered_courses(request):
    # Assuming your StudentRegistration model has a foreign key to User as 'user'
    registrations = StudentRegistration.objects.filter(user=request.user).select_related('course', 'course__schedule')
    
    return render(request, 'registered_courses.html', {'registrations': registrations})
# INSERT INTO myapp_courseschedule (days, start_time, end_time, room_number) VALUES ('Thursday, Friday', '08:00', '10:00', '303');
