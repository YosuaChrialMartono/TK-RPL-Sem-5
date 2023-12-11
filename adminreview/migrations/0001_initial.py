# Generated by Django 4.2.7 on 2023-12-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Materi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul_materi', models.CharField(max_length=200)),
                ('deskripsi', models.TextField()),
                ('status_persetujuan', models.CharField(default='Menunggu Persetujuan', max_length=20)),
                ('feedback', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
