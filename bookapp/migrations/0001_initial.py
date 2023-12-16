# Generated by Django 4.1.13 on 2023-12-16 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bid', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=20)),
                ('short_desc', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('issue', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Book',
            },
        ),
        migrations.CreateModel(
            name='issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.CharField(max_length=5)),
                ('sid', models.CharField(max_length=5)),
                ('uid', models.CharField(max_length=5, null=True)),
                ('req_date', models.DateTimeField()),
                ('issue_date', models.DateField(null=True)),
                ('return_date', models.DateField(null=True)),
                ('close_date', models.DateTimeField(null=True)),
                ('actions', models.CharField(default='0', max_length=1)),
            ],
            options={
                'db_table': 'issue',
            },
        ),
    ]