# Generated by Django 3.1 on 2020-09-09 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='myblog',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
