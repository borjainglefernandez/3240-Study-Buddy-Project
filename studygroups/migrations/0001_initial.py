# Generated by Django 3.1.1 on 2020-10-19 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('studentprofile', '0012_delete_studygroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoomInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('maxSize', models.PositiveSmallIntegerField(default=2)),
                ('members', models.ManyToManyField(to='studentprofile.Student')),
                ('zoom', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='studygroups.zoominfo')),
            ],
        ),
    ]