from django.urls import path
from .views import Login, teacher_admin, student_admin, courses_teach, Logout, homeworks, homeworkdetail, course_detail, \
    QR, detail_question, add_question, course_detail_student, homeworks_for_course, homeworks_for_student, \
    homework_detail_student, questions_student_side, response_student_side, get_responses_question, clean_view, \
    teacher_video, student_video, student_video_course, homeworks_for_student_det, homeworks_det

urlpatterns = [
    path('', Login, name="login"),
    path('student/', student_admin, name="home-student"),
    path('teacher/', teacher_admin, name="home-teacher"),
    path('courses-teach/', courses_teach, name="courses-teach"),
    path('logout/', Logout, name="logout"),
    path('homework/', homeworks, name="homework"),
    path('teacher-video/', teacher_video, name="teacher-video"),
    path('student-video/', student_video, name="student-video"),
    path('student-video-course/<str:pk>', student_video_course, name="student-video-course"),
    path('homework-student-det/<str:pk>', homeworks_for_student_det, name="student-homeworks-det"),
    path('homework-det/<str:pk>', homeworks_det, name="homeworks-det"),
    path('homework-detail/<str:id>', homeworkdetail, name="homework-detail"),
    path('course-detail/<str:id>', course_detail, name="course-detail"),
    path('course-detail-student/<str:id>', course_detail_student, name="course-detail-student"),
    path('question_response/', QR, name="questions"),
    path('questions_student_side/', questions_student_side, name="question-student"),
    path('question_detail/<str:pk>', detail_question, name="detail-question"),
    path('question_detail_student/<str:pk>', response_student_side, name="detail-question-student"),
    path('get_responses/<str:pk>', get_responses_question, name="get-responses"),
    path('homework_student/<str:pk>', homeworks_for_course, name="homework-for-course"),
    path('homeworks_student_side/', homeworks_for_student, name="homework-for-student"),
    path('add_question/', add_question, name="add-question"),
    path('clean/', clean_view, name="clean-view"),
    path('homework-detail-student/<str:pk>', homework_detail_student, name="homework-detail-student"),
]
