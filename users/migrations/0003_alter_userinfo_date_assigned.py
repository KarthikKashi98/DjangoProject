# Generated by Django 4.1.5 on 2023-01-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userinfo_date_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='date_assigned',
            field=models.DateField(auto_now_add=True),
        ),
    ]