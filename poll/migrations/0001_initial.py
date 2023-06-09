# Generated by Django 4.2 on 2023-04-29 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200, verbose_name='متن سوال')),
                ('date published', models.DateTimeField(verbose_name='تاریخ انتشار')),
            ],
        ),
        migrations.CreateModel(
            name='Choise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choise_text', models.CharField(max_length=200, verbose_name='متن گزینه')),
                ('votes', models.IntegerField(default=0, verbose_name='تعداد رای')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.question')),
            ],
        ),
    ]
