# Generated by Django 2.0 on 2018-01-21 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20180118_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
