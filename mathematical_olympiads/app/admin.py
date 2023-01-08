from django.contrib import admin

from .models import Olympiad, Task, Answer


class OlympiadAdmin(admin.ModelAdmin):
    list_display = ("title", "olympiad_level", "created", "start_time", "end_time")
    search_fields = ("title",)
    list_filter = ("created",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "correct_answer", "created")
    search_fields = ("text",)
    list_filter = ("created",)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "answer", "is_correct", "answer_created")
    list_filter = ("user",)


admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Answer, AnswerAdmin)
