from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import os
from .models import Student, Enquiry, Courses
from django.utils import timezone




def home(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')


def admission(request):
    return render(request, 'admission.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "myadmin/login.html", {"error": "invalid username or password"})
    return render(request, "myadmin/login.html")


def studentlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(email=email, password=password)

            request.session["student_id"] = student.student_id
            request.session["student_name"] = student.name
            request.session["student_email"] = student.email

            return redirect("studentdash")

        except Student.DoesNotExist:
            return render(
                request,
                "student/studentlogin.html",
                {"error": "Invalid email or password"}
            )

    return render(request, "student/studentlogin.html")


def studentdash(request):
    if "student_id" not in request.session:
        return redirect("studentlogin")

    student = Student.objects.get(student_id=request.session["student_id"])

    return render(request, "student/studentdash.html", {"student": student})


def addstu(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        

        Student.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            application_status="Pending",
            payment_status="pending",
        )

        return redirect('add')
    return render(request, 'myadmin/add.html')


@login_required(login_url='admin_login')
def dashboard(request):
    students = Student.objects.all()
    return render(request, 'myadmin/dashboard.html', {'students': students})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def add(request):
    return render(request, "myadmin/add.html")


def enquiry(request):
    courses = Courses.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        course = request.POST.get('course')
        message = request.POST.get('message')

        Enquiry.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            course=course,
            message=message,
        )

        send_mail(
            subject="Thank You for Your Enquiry",
            message=f"""
Dear {name},

Thank you for contacting Sipher Web Academy.

We have successfully received your enquiry regarding "{course}".

Our team will contact you shortly.

Regards,
Sipher Web Academy
Lucknow
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('enquiry')

    return render(request, "enquiry.html", {
        "courses": courses,
    })



def adminenquiry(request):
    enquiries = Enquiry.objects.all()
    return render(request, 'myadmin/adminenquiry.html', {'enquiries': enquiries})


def adminenquiry_delete(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)
    enquiry.delete()
    return redirect('adminenquiry')


def admincourses(request):
    courses = Courses.objects.all().order_by('coursename')
    return render(request, 'myadmin/admincourses.html', {'courses': courses})


def addcourse(request):
    if request.method == 'POST':
        courseimg = request.FILES.get('courseimg')
        coursename = request.POST.get('coursename')
        session = request.POST.get('session')
        duration = request.POST.get('duration')
        fees = request.POST.get('fees')

        Courses.objects.create(
            coursename=coursename,
            session=session,
            duration=duration,
            fees=fees,
            courseimg=courseimg,   
        )

        return redirect('admincourses')

    return render(request, 'myadmin/addcourse.html')

def addcourse_delete(request, id):
    course = get_object_or_404(Courses, course_id=id)
    course.delete()
    return redirect('admincourses')


def addcourse_edit(request, id):
    course = get_object_or_404(Courses, course_id=id)

    if request.method == "POST":
        course.courseimg = request.FILES.get("courseimg") 
        course.coursename = request.POST.get("coursename")
        course.session = request.POST.get("session")
        course.duration = request.POST.get("duration")
        course.fees = request.POST.get("fees")
        course.save()

        return redirect("admincourses")

    return render(request, "myadmin/admincourses.html", {"course": course, "courses": Courses.objects.all()})


def allstudents(request):
    students = Student.objects.all()
    return render(request, 'myadmin/allstudents.html', {'students': students})


def allstudents_delete(request, id):
    student = get_object_or_404(Student, student_id=id)
    student.delete()
    return redirect('allstudents')


def allstudents_edit(request, id):
    student = get_object_or_404(Student, student_id=id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.mobile = request.POST.get("mobile")
        student.password = request.POST.get("password")
        student.save()

    return redirect("allstudents")


def allstudents_status(request, id):
    student = get_object_or_404(Student, student_id=id)

    if request.method == "POST":
        student.application_status = request.POST.get("status")
        student.save()

    return redirect("allstudents")


def studentcourse(request):
    course=Student.objects.get(student_id=request.session["student_id"]).course
    courses=Courses.objects.filter(coursename=course)
    return render(request, 'student/studentcourse.html',{"courses":courses})


def studentfees(request):
    student_email = request.session.get("student_email")

    if not student_email:
        return redirect("studentlogin")

    student = get_object_or_404(Student, email=student_email)
    course = Courses.objects.filter(coursename=student.course).first()
    if course is None:
        return render(request, "student/studentfees.html", {
            "student": student,
            "error": "Please complete your course selection before submitting fees."
        })

    if request.method == "POST":
        student.payment_screenshot = request.FILES.get("payment_screenshot")
        student.payment_status = "submitted"
        student.application_status = "Fees Submitted"
        student.save()

        return redirect("studentfees")

    return render(request, "student/studentfees.html", {
        "student": student,
        "course": course
    })


def studentapplication(request):
    student_email = request.session.get("student_email")

    if not student_email:
        return redirect("studentlogin")

    student = get_object_or_404(Student, email=student_email)
    courses = Courses.objects.all()

    if request.method == "POST":

        if student.application_status in [
            "Document Verified",
            "Fees Submitted",
            "Enrolled"
        ]:
            return redirect("studentapplication")

        student.name = request.POST.get("name")
        student.dob = request.POST.get("dob")
        student.age = request.POST.get("age")
        student.gender = request.POST.get("gender")
        student.email = request.POST.get("email")
        student.mobile = request.POST.get("mobile")
        student.blood_group = request.POST.get("blood_group")
        student.father_name = request.POST.get("father_name")
        student.father_mobile = request.POST.get("father_mobile")
        student.class10 = request.POST.get("class10")
        student.class12 = request.POST.get("class12")
        student.course = request.POST.get("course")
        student.aadhaar = request.POST.get("aadhaar")
        student.address = request.POST.get("address")

        password = request.POST.get("password")
        if password:
            student.password = password

        safe_email = student.email.replace("@", "_").replace(".", "_")

        upload_fields = {
            "student_photo": "student_photo",
            "aadhaar_photo": "aadhaar_photo",
        }

        for field, label in upload_fields.items():
            uploaded_file = request.FILES.get(field)

            if uploaded_file is not None:
                extension = os.path.splitext(uploaded_file.name)[1]
                uploaded_file.name = f"{safe_email}_{label}{extension}"
                setattr(student, field, uploaded_file)

        if student.application_status == "Pending":
            student.application_status = "Document Verified"

        student.save()

        return redirect("studentapplication")

    return render(request, "student/studentapplication.html", {
        "student": student,
        "courses": courses,
    })

def adminapplication(request):
    students = Student.objects.all()
    return render(request, 'myadmin/adminapplication.html', {'students': students})


def adminapplication_delete(request, id):
    student = get_object_or_404(Student, student_id=id)
    student.delete()
    return redirect('adminapplication')


def student_fee_submission(request):
    student_email = request.session.get("student_email")
    if not student_email:
        return redirect("studentlogin")
    student = get_object_or_404(Student, email=student_email)

    course = Courses.objects.filter(coursename=student.course).first()
    if course is None:
        return render(request, "student/studentapplication.html", {
            "student": student,
            "error": "Please complete your course selection before submitting fees."
        })

    if request.method == "POST":
        student.payment_screenshot = request.FILES.get("payment_screenshot")
        student.payment_status = "submitted"
        student.application_status = "Fees Submitted"
        student.save()

        return redirect("student_fee_submission")
    return render(request, "student/student_fee_submission.html", {"student": student, "course": course})


def payment_success(request):
    student_email = request.session.get("student_email")
    if not student_email:
        return redirect("studentlogin")
    student = get_object_or_404(Student, email=student_email)
    student.payment_status = "verified"
    student.application_status = "Fees Submitted"
    student.save()
    return redirect("studentdash")


def fee_status(request):
    students = Student.objects.all()
    for student in students:
        try:
            course = Courses.objects.get(coursename=student.course)
            student.course_fees = course.fees
        except Courses.DoesNotExist:
            student.course_fees = 0

    return render(request, "myadmin/fee_status.html", {"students": students})


def verify_payment(request, id):
    student = get_object_or_404(Student, student_id=id)
    student.payment_status = "verified"
    student.save()
    return redirect("fee_status")


def rejected_payment(request, id):
    student = get_object_or_404(Student, student_id=id)
    student.payment_status = "rejected"
    student.save()
    return redirect("fee_status")

def courses(request):
    courses = Courses.objects.all().order_by("coursename")

    fee_values = []
    for c in courses:
        try:
            fee_values.append(float(c.fees))
        except (TypeError, ValueError):
            pass

    avg_fee = int(sum(fee_values) / len(fee_values)) if fee_values else 0

    return render(request, "courses.html", {
        "courses": courses,
        "avg_fee": avg_fee,
    })


    