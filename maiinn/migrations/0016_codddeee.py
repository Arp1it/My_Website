# Generated by Django 4.1.5 on 2023-04-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maiinn', '0015_alter_userprofile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codddeee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('gmmaail', models.CharField(max_length=50)),
            ],
        ),
    ]
