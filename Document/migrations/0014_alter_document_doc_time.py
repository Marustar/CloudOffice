# Generated by Django 4.1 on 2023-06-15 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Document', '0013_alter_document_doc_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='Doc_Time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
