# Generated by Django 2.0.2 on 2018-03-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeload', '0005_solutions_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutions',
            name='tests_passed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='test_file',
            field=models.FileField(default=None, upload_to='solution_tests/'),
            preserve_default=False,
        ),
    ]
