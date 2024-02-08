# Generated by Django 4.2.1 on 2024-01-08 00:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0011_citation_date_creation_alter_process_timetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]