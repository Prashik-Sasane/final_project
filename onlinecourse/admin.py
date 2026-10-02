from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .models import (
    Choice,
    Course,
    Lesson,
    Question,
    Submission,
    Instructor,
    Learner,
)


# Authentication and Authorization
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)


# Course -> Questions -> Choices
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "course")
    search_fields = ["title", "course__name"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "lesson")
    search_fields = ["question_text"]


# Required OnlineCourse models
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)