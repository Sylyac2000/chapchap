# Generated by Django 3.2.11 on 2022-12-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
