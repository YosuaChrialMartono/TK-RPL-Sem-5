# Generated by Django 4.2.7 on 2023-12-04 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authuser', '0004_remove_mentor_user_delete_mentee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
