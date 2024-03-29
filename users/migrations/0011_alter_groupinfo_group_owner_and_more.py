# Generated by Django 4.1.5 on 2023-03-15 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_groupinfo_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinfo',
            name='group_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.main_user_info'),
        ),
        migrations.AlterField(
            model_name='groupsmembers',
            name='member_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.main_user_info'),
        ),
    ]
