# Generated by Django 3.0.5 on 2021-08-06 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_user', models.CharField(max_length=200)),
                ('chat_bot', models.CharField(max_length=200)),
            ],
        ),
    ]
