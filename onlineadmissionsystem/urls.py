
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from admissionapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admission/', views.admission, name='admission'),
    path('courses/', views.courses, name='courses'),
    path('enquiry/', views.enquiry, name='enquiry'),

    path('myadmin/login/',views.admin_login, name='admin_login'),
    path('myadmin/dashboard/',views.dasboard, name='dashboard'),
    path('logout/',views.admin_logout, name='admin_logout'),
    path('myadmin/add/',views.add, name='add'),
    path('myadmin/adminenquiry/',views.adminenquiry, name='adminenquiry'),
    path('myadmin/adminenquiry/<int:id>/delete/',views.adminenquiry_delete, name='adminenquiry_delete'),
    path('addstu/',views.addstu, name='addstu'),

    path('allstudents/',views.allstudents, name='allstudents'),
    path('allstudents/<int:id>/delete/',views.allstudents_delete, name='allstudents_delete'),
    path('allstudents/<int:id>/edit/',views.allstudents_edit, name='allstudents_edit'),
    path('allstudents/<int:id>/status/',views.allstudents_status, name='allstudents_status'),
    path('student/studentlogin/',views.studentlogin, name='studentlogin'),
    path('studentdash/',views.studentdash, name='studentdash'),

    path('myadmin/admincourses/',views.admincourses, name='admincourses'),
    path('myadmin/addcourses/<int:id>/edit/',views.addcourse_edit, name='addcourse_edit'),
    path('myadmin/addcourses/<int:id>/delete/',views.addcourse_delete, name='addcourse_delete'),
    path('addcourse/',views.addcourse, name='addcourse'),

    path('student/studentcourse/',views.studentcourse, name='studentcourse'),
    path('student/studentfees/',views.studentfees, name='studentfees'),
    path('student/studentapplication/',views.studentapplication, name='studentapplication'),
    path('myadmin/adminapplication/',views.adminapplication, name='adminapplication'),
    path('adminapplication/<int:id>/delete/',views.adminapplication_delete, name='adminapplication_delete'),

    path('student_fee_submission/',views.student_fee_submission, name='student_fee_submission'),
    path('fee_status/',views.fee_status, name='fee_status'),
    path('verify_payment/<int:id>/',views.verify_payment, name='verify_payment'),
    path('rejected_payment/<int:id>/',views.rejected_payment, name='rejected_payment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)