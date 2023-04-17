# Generated by Django 3.2.18 on 2023-04-17 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File_Name', models.CharField(max_length=100)),
                ('File_Extend', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('Doc_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Doc_Title', models.CharField(max_length=50)),
                ('Doc_Type', models.IntegerField()),
                ('Doc_State', models.IntegerField()),
                ('Doc_Dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.departments')),
                ('Doc_Files', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Document.files')),
                ('Doc_Reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Doc_Reciever', to='User.users')),
                ('Doc_Sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Doc_Sender', to='User.users')),
            ],
        ),
    ]
