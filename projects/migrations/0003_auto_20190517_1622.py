# Generated by Django 2.2 on 2019-05-17 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_datepoint_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datepoint',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]