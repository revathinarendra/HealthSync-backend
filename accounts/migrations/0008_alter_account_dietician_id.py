# Generated by Django 5.2.4 on 2025-07-27 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_account_dietician_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='dietician_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
