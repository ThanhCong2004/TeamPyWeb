# Generated by Django 5.0.14 on 2025-05-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_appuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'USERS',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='AppUser',
        ),
    ]
