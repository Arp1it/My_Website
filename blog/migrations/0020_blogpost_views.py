# Generated by Django 4.1.5 on 2023-04-28 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_blogviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='views',
            field=models.IntegerField(default=1),
        ),
    ]
