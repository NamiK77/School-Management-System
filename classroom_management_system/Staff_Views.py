from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Staff,Staff_Notification,Staff_leave,Staff_Feedback,Subject,Session_Year,Student,StudentResult
from django.contrib import messages



@login_required(login_url='/')
def HOME(request):
    return render(request,'Staff/home.html')

@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin= request.user.id)
    for i in staff:
        staff_id = i.id

        notification = Staff_Notification.objects.filter(staff_id = staff_id)

        context = {
            'notification': notification,
        }
        return render(request,'Staff/notification.html',context)

@login_required(login_url='/')
def STAFF_NOTIFICATIONS_MARK_AS_DONE(request,status):
    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications')

@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        staff_leave_history = Staff_leave.objects.filter(staff_id = staff_id)
        context ={
            'staff_leave_history':staff_leave_history,
        }
        return render(request,'Staff/apply_leave.html',context)

@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin = request.user.id)

        leave = Staff_leave(
            staff_id = staff,
            data = leave_date,
            message = leave_message

        )
        messages.success(request,'Leave Successfully Sent ')

        leave.save()
        return redirect('staff_apply_leave')

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)

    context = {
        'feedback_history':feedback_history
    }
    return render(request,'Staff/feedback.html',context)

@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        staff = Staff.objects.get(admin = request.user.id)
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = "",

        )
        feedback.save()
        return redirect('staff_feedback')

@login_required(login_url='/')
def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin = request.user.id)

    subject= Subject.objects.filter(staff = staff_id)
    session_year = Session_Year.objects.all()
    context = {
        'subject': subject,
        'session_year':session_year,
    }
    return render(request,'Staff/take_attendance.html',context)


def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin=request.user.id)

    subjects = Subject.objects.filter(staff_id=staff)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            get_subject = Subject.objects.get(id=subject_id)
            get_session = Session_Year.objects.get(id=session_year_id)
            subjects = Subject.objects.filter(id=subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        'subjects': subjects,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'students': students,
    }

    return render(request, 'Staff/add_result.html', context)



def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id=subject_id)

        check_exists = StudentResult.objects.filter(subject_id = get_subject, student_id = get_student).exists()
        if check_exists:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_mark = assignment_mark
            result.exam_mark = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_add_result')
        else:
            result = StudentResult(student_id = get_student,
                                   subject_id = get_subject,
                                   exam_mark = Exam_mark,
                                   assignment_mark = assignment_mark)
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('staff_add_result')