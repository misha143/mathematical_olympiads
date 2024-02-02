from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("results/<int:olympiad_level>",views.get_results, name="get_results"),
    path("olympiad/<int:pk_olympiad>/early_completion", views.olympiad_early_completion,
         name="olympiad_early_completion"),
    path("olympiad/<int:pk_olympiad>/task/<int:pk_task>", views.task_view, name="task"),
    path("olympiad2/<int:pk_olympiad>/task/<int:pk_task>", views.task_view2, name="task2"),
]
