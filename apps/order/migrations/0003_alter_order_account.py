# Generated by Django 3.2.3 on 2021-05-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0002_auto_20210527_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='account',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
