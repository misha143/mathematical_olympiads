import math

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Olympiad(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название олимпиады")
    description = models.CharField(max_length=600, verbose_name="Описание олимпиады")

    LEVELS = (
        ('1', '1 тур'),
        ('2', '2 тур'),
    )
    olympiad_level = models.CharField(max_length=1, choices=LEVELS, unique=True, verbose_name="Тур олимпиады")

    image_url = models.CharField(blank=False, max_length=300, verbose_name="Ссылка на обложку олимпиады",
                                 help_text="Загрузите её на imgur.com/upload После этого правым кликом мыши нажмите по фото и кликните 'Копировать ссылку на изображение'. Вставьте ссылку. Пример: https://i.imgur.com/sRjy27f.jpg")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Олимпиада создана")
    start_time = models.DateTimeField(verbose_name="Время старта олимпиады")
    end_time = models.DateTimeField(verbose_name="Время окончания олимпиады")

    ATTEMPTS = (
        (1, '1 попытка'),
        (2, '2 попытки'),
        (3, '3 попытки'),
        (4, '4 попытки'),
        (5, '5 попыток'),
    )
    number_of_attempts = models.IntegerField(choices=ATTEMPTS, unique=True, verbose_name="Количество попыток отправки решения для каждого задания 2 тура олимпиады (если у вас 1 тур, то выберите любое)")

    class Meta:
        verbose_name = 'Олимпиада'
        verbose_name_plural = 'Олимпиады'

        ordering = ['-created']

        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F("start_time")),
                                   name='Время окончания должно быть позже времени старта'),
        ]

    def __str__(self):
        return self.title

    def display_olympiad_level(self):
        for i in self.LEVELS:
            if i[0] == self.olympiad_level:
                return i[1]


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок задания")
    text = models.TextField(verbose_name="Текст задания")
    correct_answer = models.FloatField(verbose_name="Правильный ответ",
                                       help_text="Доступен только ввод числа, например: 1,35 или 17")
    image_url = models.CharField(blank=True, max_length=200, verbose_name="Ссылка на иллюстрацию",
                                 help_text="Если в постановке задания требуется иллюстрация, то загрузите её на imgur.com/upload После этого правым кликом мыши нажмите по фото и кликните 'Копировать ссылку на изображение'. Вставьте ссылку. Пример: https://i.imgur.com/sRjy27f.jpg")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Задание создано")
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name="Олимпиада")

    class Meta:
        ordering = ['-created']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title


class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Задание")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Команда")
    answer = models.FloatField(verbose_name="Ответ")
    is_correct = models.BooleanField(verbose_name="Правильно ответили?")
    answer_created = models.DateTimeField(verbose_name="Когда ответили? (UTC+5)", auto_now_add=True, blank=True,
                                          null=True)
    attempt_number = models.PositiveSmallIntegerField(verbose_name="Номер попытки", blank=True, null=True)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        unique_together = (
            'task',
            'user',
        )

    def __str__(self):
        return f"{self.task}"


class Timetrack(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name="Олимпиада")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Команда")
    start_time = models.DateTimeField(verbose_name="Когда приступили к выполнению? (UTC+5)", auto_now_add=True,
                                      blank=True,
                                      null=True)
    end_time = models.DateTimeField(verbose_name="Когда закончили выполнять? (UTC+5)",
                                    blank=True,
                                    null=True)

    class Meta:
        verbose_name = 'Время прохождения'
        verbose_name_plural = 'Время прохождения'
        unique_together = (
            'olympiad',
            'user',
        )

    def __str__(self):
        return f"{math.ceil((self.end_time - self.start_time).total_seconds())}"
