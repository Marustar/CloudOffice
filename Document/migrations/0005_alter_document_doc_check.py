# Generated by Django 3.2.16 on 2023-06-14 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Document', '0004_document_doc_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='Doc_Check',
            field=models.IntegerField(),
        ),
    ]
