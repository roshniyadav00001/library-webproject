# Generated by Django 5.0 on 2024-03-26 15:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_delete_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('pincode', models.ImageField(upload_to='')),
                ('address', models.TextField()),
                ('orderamt', models.FloatField(null=True)),
                ('payment_mode', models.CharField(max_length=100)),
                ('trackingno', models.CharField(max_length=100, null=True)),
                ('order_date', models.DateField()),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('confirm', 'Confirm'), ('deliver', 'Deliver'), ('cancel', 'Canceled'), ('return', 'Return'), ('refund', 'Refund')], default='pending', max_length=100)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=100, null=True)),
                ('order_qty', models.IntegerField(default=1)),
                ('orderdate', models.DateField(auto_now_add=True)),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.mybook')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='orderTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('status_date', models.DateField(auto_now_add=True)),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.mybook')),
                ('trackingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.orderitems')),
            ],
        ),
        migrations.CreateModel(
            name='state',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.country')),
            ],
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.state')),
            ],
        ),
    ]
