# Generated by Django 3.2 on 2022-04-11 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0002_auto_20220408_1855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='closeschedulemodel',
            old_name='ending_date',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='closeschedulemodel',
            old_name='ending_hour',
            new_name='end_hour',
        ),
        migrations.RenameField(
            model_name='closeschedulemodel',
            old_name='starting_date',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='closeschedulemodel',
            old_name='starting_hour',
            new_name='start_hour',
        ),
        migrations.RenameField(
            model_name='openschedulemodel',
            old_name='ending_date',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='openschedulemodel',
            old_name='ending_hour',
            new_name='end_hour',
        ),
        migrations.RenameField(
            model_name='openschedulemodel',
            old_name='starting_date',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='openschedulemodel',
            old_name='starting_hour',
            new_name='start_hour',
        ),
        migrations.RenameField(
            model_name='professionalschedulemodel',
            old_name='ending_hour',
            new_name='end_hour',
        ),
        migrations.AlterField(
            model_name='closeschedulemodel',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='professionalmodel',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this professional should be treated as active. Unselect this instead of deleting professional.', verbose_name='professional business active'),
        ),
    ]
