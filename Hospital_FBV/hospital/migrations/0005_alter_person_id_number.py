# Generated by Django 3.2.13 on 2022-05-11 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_alter_person_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='id_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
