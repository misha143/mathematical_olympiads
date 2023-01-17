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

    # олимпиада 1 ждёт начала
    olimp1_waiting_to_begin = Olympiad.objects.filter(olympiad_level='1', start_time__gt=timezone.now())
    olimp1_waiting_to_begin_seconds = 0
    if olimp1_waiting_to_begin:
        olimp1_waiting_to_begin_seconds = math.ceil((getattr(olimp1_waiting_to_begin[0], 'start_time') - timezone.now()).total_seconds()) + 1

    return render(request, 'index.html', {
        "olimp1_finished": olimp1_finished,
        "olimp1_work": olimp1_work,
        "olimp1_waiting_to_begin": olimp1_waiting_to_begin,
        "olimp1_waiting_to_begin_seconds": olimp1_waiting_to_begin_seconds,
    })
