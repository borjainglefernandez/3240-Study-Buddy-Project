# Generated by Django 3.1.1 on 2020-10-06 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentprofile', '0003_student_major'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
