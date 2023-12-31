# Generated by Django 4.1.13 on 2023-12-16 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('uid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('phone_no', models.CharField(max_length=12)),
            ],
            options={
                'db_table': 'Librarian',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('roll', models.IntegerField()),
                ('dept', models.CharField(max_length=10)),
                ('reg', models.CharField(max_length=10, unique=True)),
                ('address', models.CharField(max_length=50)),
                ('phone_no', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=150)),
                ('checked', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('checked_by', models.CharField(default='', max_length=20)),
            ],
            options={
                'db_table': 'Student',
            },
        ),
    ]
