# Generated by Django 4.1.7 on 2023-05-20 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.CharField(default='sdfsdf', max_length=1000),
            preserve_default=False,
        ),
    ]