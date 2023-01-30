# Generated by Django 4.1.5 on 2023-01-17 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_answer_is_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='olympiad',
            name='olympiad_level',
            field=models.CharField(choices=[(1, '1 тур'), (2, '2 тур - основной уровень'), (3, '2 тур - высший уровень')], max_length=1, unique=True, verbose_name='Тур олимпиады'),
        ),
    ]
