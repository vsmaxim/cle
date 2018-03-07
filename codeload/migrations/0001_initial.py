# Generated by Django 2.0.2 on 2018-03-06 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solutions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.FilePathField(path='/home/vms/solutions')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255)),
                ('task_text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='solutions',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeload.Task'),
        ),
    ]
