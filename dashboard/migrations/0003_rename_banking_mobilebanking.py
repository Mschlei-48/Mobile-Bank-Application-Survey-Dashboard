# Generated by Django 4.2.5 on 2024-10-15 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_banking_pleaseprovideanyadditionalcommentsorsuggestionsregardingaienabledmobilebanking'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Banking',
            new_name='MobileBanking',
        ),
    ]
