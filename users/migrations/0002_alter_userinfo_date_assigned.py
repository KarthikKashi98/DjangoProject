# Generated by Django 4.1.5 on 2023-01-24 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='date_assigned',
            field=models.DateField(),
        ),
    ]