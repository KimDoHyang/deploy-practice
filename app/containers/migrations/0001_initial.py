# Generated by Django 2.1.2 on 2018-12-16 16:07

import containers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppTrailerContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=50, null=True, verbose_name='코멘트')),
                ('posting_img', models.ImageField(blank=True, null=True, upload_to=containers.models.trailer_directory_path, verbose_name='영화 이미지')),
            ],
            options={
                'verbose_name': '앱 영화 트레일러(MOVIE SELECTION)',
                'verbose_name_plural': '앱 영화 트레일러(MOVIE SELECTION) 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='EventContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='이벤트명')),
                ('container_img', models.ImageField(blank=True, null=True, upload_to=containers.models.event_directory_path, verbose_name='이벤트 이미지')),
                ('container_link', models.URLField(blank=True, default='', null=True, verbose_name='이벤트 링크')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화')),
            ],
            options={
                'verbose_name': '이벤트(중단) 구성',
                'verbose_name_plural': '이벤트(중단) 구성 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='EventFooterContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='이벤트명')),
                ('container_img', models.ImageField(blank=True, null=True, upload_to=containers.models.event_directory_path, verbose_name='이벤트 이미지')),
                ('container_link', models.URLField(blank=True, default='', null=True, verbose_name='이벤트 링크')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화')),
            ],
            options={
                'verbose_name': '이벤트(하단) 구성',
                'verbose_name_plural': '이벤트(하단) 구성 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='MainContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='이벤트명')),
                ('posting_start', models.DateTimeField(verbose_name='포스팅 시작')),
                ('posting_end', models.DateTimeField(verbose_name='포스팅 종료')),
                ('container_img', models.ImageField(blank=True, null=True, upload_to=containers.models.event_directory_path, verbose_name='이벤트 이미지')),
                ('container_link', models.URLField(blank=True, default='', null=True, verbose_name='이벤트 링크')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='활성화')),
            ],
            options={
                'verbose_name': '메인 이벤트(상단) 구성',
                'verbose_name_plural': '메인 이벤트(상단) 구성 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='WebTrailerContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posting_img', models.ImageField(blank=True, null=True, upload_to=containers.models.trailer_directory_path, verbose_name='영화 이미지')),
            ],
            options={
                'verbose_name': '웹 영화 트레일러(MOVIE SELECTION)',
                'verbose_name_plural': '웹 영화 트레일러(MOVIE SELECTION) 목록',
                'ordering': ['pk'],
            },
        ),
    ]
