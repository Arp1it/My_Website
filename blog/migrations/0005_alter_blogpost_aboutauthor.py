# Generated by Django 4.1.5 on 2023-02-03 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogpost_aboutauthor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='aboutauthor',
            field=models.CharField(max_length=50),
        ),
    ]
