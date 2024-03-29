# Generated by Django 3.1.6 on 2021-02-09 17:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210207_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('code', models.CharField(max_length=200, unique=True)),
                ('price', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=True)),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.DeleteModel(
            name='Wood',
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='child',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='products.product'),
        ),
    ]
