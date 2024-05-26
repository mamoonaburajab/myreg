from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
      path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('courses/', views.course_list, name='course_list'),
    path('register_course/<int:course_id>/', views.register_course, name='register_course'),
    path('my_courses/', views.registered_courses, name='my_courses'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
