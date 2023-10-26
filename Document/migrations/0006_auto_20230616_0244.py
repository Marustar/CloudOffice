# Generated by Django 3.2.16 on 2023-06-15 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Document', '0005_alter_document_doc_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='Doc_Comment',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='Doc_Time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='Doc_Check',
            field=models.IntegerField(null=True),
        ),
    ]