# Generated by Django 4.2.5 on 2024-10-15 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banking',
            name='PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking',
            field=models.CharField(max_length=5000),
        ),
    ]
