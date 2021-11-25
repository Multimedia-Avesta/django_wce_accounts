# Generated by Django 2.2 on 2021-02-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_user_initials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='public_name',
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.TextField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
