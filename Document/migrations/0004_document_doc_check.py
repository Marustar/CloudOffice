# Generated by Django 3.2.16 on 2023-06-14 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Document', '0003_document_doc_content_alter_document_doc_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='Doc_Check',
            field=models.IntegerField(null=True),
        ),
    ]