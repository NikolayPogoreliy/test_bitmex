# Generated by Django 3.2.3 on 2021-05-24 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=20, unique=True)),
                ('symbol', models.CharField(max_length=6)),
                ('volume', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('side', models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')], default='Buy', max_length=4)),
                ('price', models.IntegerField(null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
    ]
