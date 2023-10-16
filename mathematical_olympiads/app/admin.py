from django.contrib import admin

from .models import Olympiad, Task, Answer, Timetrack


class OlympiadAdmin(admin.ModelAdmin):
    list_display = ("title", "olympiad_level", "start_time", "end_time", "created")


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "olympiad", "text", "correct_answer", "created")
    search_fields = ("text",)
    list_filter = ("created",)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "answer", "is_correct", "answer_created", "attempt_number")
    list_filter = ("user",)


class TimetrackAdmin(admin.ModelAdmin):
    list_display = ("olympiad", "user", "start_time", "end_time")
    list_filter = ("user", "olympiad",)


admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Timetrack, TimetrackAdmin)
