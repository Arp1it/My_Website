# Generated by Django 4.1.5 on 2023-03-28 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0018_delete_blogviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogViews',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('asss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
