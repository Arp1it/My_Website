# Generated by Django 4.1.5 on 2023-03-28 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blogviews_asss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogviews',
            name='asss',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost'),
        ),
    ]
