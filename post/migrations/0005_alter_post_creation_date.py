# Generated by Django 3.2.7 on 2021-09-19 08:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0004_auto_20210918_2126"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="creation_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
