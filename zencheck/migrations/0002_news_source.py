# Generated by Django 3.0.8 on 2020-08-06 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zencheck', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
