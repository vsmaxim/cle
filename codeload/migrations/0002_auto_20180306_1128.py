# Generated by Django 2.0.2 on 2018-03-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutions',
            name='source',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
