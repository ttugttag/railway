# Generated by Django 5.1.2 on 2024-10-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0002_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='artist',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
