# Generated by Django 3.0.5 on 2021-02-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('API', '0002_delete_modelthemdau'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_user', models.TextField(max_length=200)),
                ('chat_bot', models.TextField(max_length=200)),
            ],
        ),
    ]
