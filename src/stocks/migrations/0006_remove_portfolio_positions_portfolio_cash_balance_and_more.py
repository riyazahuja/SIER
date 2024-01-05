# Generated by Django 5.0.1 on 2024-01-03 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_alter_price_data_alter_stock_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='positions',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='cash_balance',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=15),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shares', models.IntegerField()),
                ('order_type', models.CharField(choices=[('B', 'Buy'), ('S', 'Sell')], help_text='B for buy, S for sell', max_length=1)),
                ('transaction_date', models.DateField()),
                ('price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.price')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),
            ],
        ),
        migrations.AddField(
            model_name='portfolio',
            name='orders',
            field=models.ManyToManyField(to='stocks.order'),
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]
