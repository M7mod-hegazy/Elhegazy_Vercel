# Generated by Django 4.0.4 on 2022-05-07 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20210722_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='qr_code',
        ),
    ]
