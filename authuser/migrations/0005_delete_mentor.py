# Generated by Django 4.2.7 on 2023-12-04 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0004_remove_mentor_user_delete_mentee'),
        ('kelas', '0003_kelas_mentee_kelas_alter_kelas_mentor_kelas_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mentor',
        ),
    ]