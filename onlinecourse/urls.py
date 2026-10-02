from django.urls import path

from . import views

app_name = "onlinecourse"

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("courses/<int:course_id>/submit/", views.submit, name="submit"),
    path("courses/<int:course_id>/result/<int:submission_id>/", views.show_exam_result, name="show_exam_result"),
]
