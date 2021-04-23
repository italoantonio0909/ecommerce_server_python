# Generated by Django 3.0.7 on 2021-04-14 13:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
        ('billing', '0001_initial'),
        ('addresses', '0002_address_billing_profile'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('refunded', models.BooleanField(default=False)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='billing.BillingProfile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shipping_address_final', models.TextField(blank=True, null=True)),
                ('billing_address_final', models.TextField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded')], default='created', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='billing_address', to='addresses.Address')),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='billing.BillingProfile')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='carts.Cart')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipping_address', to='addresses.Address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]