# Generated by Django 5.0.3 on 2024-04-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtplnewapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
