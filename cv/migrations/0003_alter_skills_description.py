# Generated by Django 4.2.3 on 2023-07-29 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0002_rename_start_date_education_from_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skills',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
