from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Choice, Course, Question, Submission, SubmissionAnswer


def index(request):
    course = Course.objects.first()
    if course:
        return redirect("onlinecourse:course_details", course_id=course.id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": None})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


def submit(request, course_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("onlinecourse:course_details", args=[course_id]))

    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(lesson__course=course).prefetch_related("choices")

    total_marks = 0
    score = 0
    submission = Submission.objects.create(
        course=course,
        student_name=request.POST.get("student_name", "Student"),
        score=0,
    )

    for question in questions:
        selected_choice_id = request.POST.get(f"question_{question.id}")
        selected_choice = None
        if selected_choice_id:
            selected_choice = Choice.objects.filter(pk=selected_choice_id, question=question).first()

        is_correct = bool(selected_choice and selected_choice.is_correct)
        total_marks += 1
        if is_correct:
            score += 1

        SubmissionAnswer.objects.create(
            submission=submission,
            question=question,
            selected_choice=selected_choice,
            is_correct=is_correct,
        )

    submission.score = score
    submission.save(update_fields=["score"])

    return redirect("onlinecourse:show_exam_result", course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, course=course)

    answers = submission.answers.select_related("question", "selected_choice").order_by("question__id")
    total_questions = Question.objects.filter(lesson__course=course).count()

    results = []
    for answer in answers:
        results.append(
            {
                "question_text": answer.question.question_text,
                "selected_choice": answer.selected_choice.choice_text if answer.selected_choice else "No answer selected",
                "is_correct": answer.is_correct,
            }
        )

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "results": results,
            "total_questions": total_questions,
            "score": submission.score,
        },
    )
