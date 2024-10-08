# Generated by Django 5.0.7 on 2024-08-26 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name of product', max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeriveCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name of product', max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorOffering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('specification', models.TextField(blank=True, help_text='information about the particular product or service ', null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the vendor or supplier.', max_length=255, verbose_name='Vendor Name')),
                ('email', models.EmailField(blank=True, help_text='Email address of the vendor.', max_length=254, null=True, verbose_name='Vendor Email')),
                ('phone_number', models.CharField(blank=True, help_text='Contact phone number of the vendor.', max_length=20, null=True, verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, help_text='Physical address of the vendor.', null=True, verbose_name='Address')),
                ('website', models.URLField(blank=True, help_text='Website of the vendor.', null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, help_text="Description of the vendor's services or products.", null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when this vendor record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when this vendor record was last updated.', verbose_name='Updated At')),
                ('offering', models.ManyToManyField(to='vendor.vendoroffering')),
            ],
            options={
                'verbose_name': 'Vendor',
                'verbose_name_plural': 'Vendors',
                'permissions': [('can_add_offering_to_vendor', 'Can add offerings to vendor')],
            },
        ),
    ]
