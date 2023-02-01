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

from .models import Olympiad, Task, Answer, Timetrack

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
    timetracker = 0
    if olimp1_work:
        olimp1_work_to_end_seconds = math.ceil(
            (getattr(olimp1_work[0], 'end_time') - timezone.now()).total_seconds()) + 2
        try:
            first_task = Task.objects.filter(olympiad__in=olimp1_work).order_by("pk")[0:1].get()
        except:
            pass

        timetracker = Timetrack.objects.filter(olympiad__in=olimp1_work, user__username=request.user.username).first()

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
        "timetracker": timetracker,

        "olimp1_waiting_to_begin": olimp1_waiting_to_begin,
        "olimp1_waiting_to_begin_seconds": olimp1_waiting_to_begin_seconds,
    })


@login_required
def task_view(request, pk_olympiad, pk_task):
    user = get_object_or_404(User, username=request.user.username)
    task = get_object_or_404(Task, pk=pk_task)
    if request.method == 'POST':
        # пробуем найти существующий
        ans = Answer.objects.filter(user=user, task=task).first()
        # если нашли, то ставим новый ответ
        if ans:
            ans.answer = float(request.POST['user_input_number'])
            ans.is_correct = task.correct_answer == ans.answer
            ans.answer_created = timezone.now()
            ans.save()
        # если нет в базе
        else:
            Answer.objects.create(task=task, user=user, answer=float(request.POST['user_input_number']),
                                  is_correct=task.correct_answer == float(request.POST['user_input_number']))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        olympiad = get_object_or_404(Olympiad, pk=pk_olympiad)

        # пробуем найти существующий отсчёт времени
        timetracker = Timetrack.objects.filter(olympiad=olympiad, user=user).first()
        # если нет в базе
        if not timetracker:
            Timetrack.objects.create(olympiad=olympiad, user=user, end_time=olympiad.end_time)

        task = get_object_or_404(Task, pk=pk_task)
        if not (timezone.now() > getattr(olympiad, 'start_time') and timezone.now() < getattr(olympiad, 'end_time')) \
                or task.olympiad != olympiad:
            return redirect('index')

        olimp_work_to_end_seconds = math.ceil(
            (getattr(olympiad, 'end_time') - timezone.now()).total_seconds()) + 2

        # все задания олимпиады
        all_tasks = Task.objects.filter(olympiad=olympiad).order_by("pk")

        # задания олимпиады на которые ответил человек
        answered_tasks = []
        for t in all_tasks:
            if Answer.objects.filter(user=user, task=t).exists():
                answered_tasks.append(t)

        # пробуем найти существующий ответ
        answer = Answer.objects.filter(user=user, task=task).first()

        return render(request, 'task.html', {
            "olympiad": olympiad,
            "task": task,
            "answered_tasks": answered_tasks,
            "all_tasks": all_tasks,
            "answer": answer,
            "olimp_work_to_end_seconds": olimp_work_to_end_seconds,
        })


@login_required
def olympiad_early_completion(request, pk_olympiad):
    user = get_object_or_404(User, username=request.user.username)
    olympiad = get_object_or_404(Olympiad, pk=pk_olympiad)

    timetracker = Timetrack.objects.filter(olympiad=olympiad, user=user).first()
    timetracker.end_time = timezone.now()
    timetracker.save()

    return redirect('index')


@login_required
def get_csv(request, pk_olympiad):
    if request.user.is_staff:
        now = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="Results_{now}.csv"'},
        )

        writer = csv.writer(response)

        olympiad = get_object_or_404(Olympiad, olympiad_level=pk_olympiad)

        # все задания олимпиады
        all_tasks = Task.objects.filter(olympiad=olympiad)

        all_answers = Answer.objects.filter(task__in=all_tasks)

        unique_users = set()

        for a in all_answers:
            unique_users.add(a.user)

        writer.writerow(
            ['Олимпиада', 'Название команды', 'Сколько секунд потратили на решение', 'Сколько баллов заработали',
             'Всего баллов в олимпиаде', '% правильно решённых заданий'])
        for u in unique_users:
            _sec_for_solve = Timetrack.objects.filter(olympiad=olympiad, user=u).first()
            _number_of_points_scored = Answer.objects.filter(task__in=all_tasks, user=u, is_correct=True).count()

            writer.writerow(
                [olympiad, u.first_name, str(_sec_for_solve), _number_of_points_scored, len(all_tasks),
                 int(round(_number_of_points_scored / len(all_tasks), 2)*100)])

        return response
    else:
        return HttpResponseNotFound("Экспорт данных может делать только администратор")
