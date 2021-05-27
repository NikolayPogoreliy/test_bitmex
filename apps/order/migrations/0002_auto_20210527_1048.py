# Generated by Django 3.2.3 on 2021-05-27 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='author_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='account',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=36, unique=True),
        ),
    ]