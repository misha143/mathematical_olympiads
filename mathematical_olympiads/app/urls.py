from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("olympiad/<int:pk_olympiad>/task/<int:pk_task>/", views.task_view, name="task"),
]