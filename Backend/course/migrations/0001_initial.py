# Generated by Django 3.0.5 on 2021-08-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id_video', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True, verbose_name='id video on youtube')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(verbose_name='description')),
                ('total_videos', models.PositiveSmallIntegerField()),
                ('authen', models.CharField(max_length=200)),
                ('view', models.PositiveIntegerField()),
                ('image', models.URLField(default='https://iuhchatbot.xyz/course', max_length=1000)),
            ],
        ),
    ]
