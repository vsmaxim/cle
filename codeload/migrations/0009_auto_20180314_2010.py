# Generated by Django 2.0.2 on 2018-03-14 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codeload', '0008_leadership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leadership',
            name='id',
        ),
        migrations.AlterField(
            model_name='leadership',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]