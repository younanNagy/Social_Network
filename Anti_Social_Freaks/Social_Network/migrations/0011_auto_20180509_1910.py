# Generated by Django 2.0.4 on 2018-05-09 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Social_Network', '0010_merge_20180509_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date_of_post',
        ),
        migrations.AlterField(
            model_name='connection',
            name='interaction',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=11),
        ),
    ]
