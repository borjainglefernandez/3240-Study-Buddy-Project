# Generated by Django 3.1.1 on 2020-10-14 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentprofile', '0009_remove_student_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='num',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]