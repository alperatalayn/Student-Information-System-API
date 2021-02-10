from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('create-class/',views.createClass,name="create-class"),
    path('class-list/',views.classList,name="class-list"),
    path('course-list/',views.courseList,name="class-list"),
    path('user-info/',views.userInfo,name="user-info"),
    path('update-class/<str:pk>',views.updateClass,name="update-class"),
    path('add-student/<str:pk>',views.addStudentToClass,name="add-student"),
    path('choose/<str:pk>',views.chooseCourses,name="choose"),
    path('create-course/',views.createCourse,name="create-course"),
    path('student-list/',views.studentList,name="student-list"),
    path('student/<str:pk>',views.studentSingle,name="student"),
    path('register/',views.createUser),
    path('token/',TokenObtainPairView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
]