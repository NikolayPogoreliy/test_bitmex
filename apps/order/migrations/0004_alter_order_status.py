# Generated by Django 3.2.3 on 2021-05-27 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0003_alter_order_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]