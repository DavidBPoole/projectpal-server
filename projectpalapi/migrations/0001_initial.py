# Generated by Django 4.1.3 on 2024-02-19 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projectpalapi.project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('uid', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projectpalapi.category')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='projectpalapi.task')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectpalapi.user'),
        ),
    ]
