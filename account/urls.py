from django.urls import path
from account.views import *
urlpatterns = [
    path('student_signup', student_signup, name = 'signup'),
    path('student_login', student_login, name = 'student_login'),
    path('student_logout', student_logout, name = 'student_logout'),
    path('admin_signup', admin_signup, name = 'admin_signup'),
    path('admin_login', admin_login, name = 'admin_login'),
    path('admin_logout', admin_logout, name = 'admin_logout'),
    path('stds_verifiy', stds_verifiy, name = 'std_verifiy'),
    path('std_verifiy', std_verifiy, name = 'std_verifiy'),
    path('std_dashboard', std_dashboard, name = 'student dashbord'),
    path('adm_dashboard', adm_dashboard, name = 'admin dashbord'),
]