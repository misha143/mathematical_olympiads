import math

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
import csv
from collections import Counter
from django.http import HttpResponse, HttpResponseNotFound

from .models import Olympiad, Task, Answer

User = get_user_model()


@login_required
def index(request):
    # олимпиада 1 прошла когда время окончание меньше now()
    olimp1_finished = Olympiad.objects.filter(olympiad_level='1', end_time__lt=timezone.now())

    # прямо сейчас проводится олимпиада 1
    olimp1_work = Olympiad.objects.filter(olympiad_level='1', end_time__gt=timezone.now(),
                                          start_time__lt=timezone.now())
    olimp1_work_to_end_seconds = 0
    first_task = 0
    if olimp1_work:
        olimp1_work_to_end_seconds = math.ceil(
            (getattr(olimp1_work[0], 'end_time') - timezone.now()).total_seconds()) + 2
        try:
            first_task = Task.objects.filter(olympiad__in=olimp1_work).order_by("pk")[0:1].get()
        except:
            pass

    # олимпиада 1 ждёт начала
    olimp1_waiting_to_begin = Olympiad.objects.filter(olympiad_level='1', start_time__gt=timezone.now())
    olimp1_waiting_to_begin_seconds = 0
    if olimp1_waiting_to_begin:
        olimp1_waiting_to_begin_seconds = math.ceil(
            (getattr(olimp1_waiting_to_begin[0], 'start_time') - timezone.now()).total_seconds()) + 2

    return render(request, 'index.html', {
        "olimp1_finished": olimp1_finished,

        "olimp1_work": olimp1_work,
        "olimp1_work_to_end_seconds": olimp1_work_to_end_seconds,
        "first_task": first_task,

        "olimp1_waiting_to_begin": olimp1_waiting_to_begin,
        "olimp1_waiting_to_begin_seconds": olimp1_waiting_to_begin_seconds,
    })


@login_required
def task_view(request, pk_olympiad, pk_task):
    olympiad = get_object_or_404(Olympiad, pk=pk_olympiad)
    if not (timezone.now() > getattr(olympiad, 'start_time') and timezone.now() < getattr(olympiad, 'end_time')):
        return redirect('index')

    task = get_object_or_404(Task, pk=pk_task)

    olimp_work_to_end_seconds = math.ceil(
        (getattr(olympiad, 'end_time') - timezone.now()).total_seconds()) + 2

    return render(request, 'task.html', {
        "olympiad":olympiad,
        "task": task,
        "olimp_work_to_end_seconds": olimp_work_to_end_seconds,
    })
