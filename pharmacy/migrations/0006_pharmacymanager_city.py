# Generated by Django 4.2.17 on 2025-01-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0005_alter_pharmacymanager_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacymanager',
            name='city',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]
