# Generated by Django 2.2.3 on 2019-07-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsite', '0002_action_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
