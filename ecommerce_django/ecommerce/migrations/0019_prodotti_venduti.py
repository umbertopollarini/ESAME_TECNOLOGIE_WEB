# Generated by Django 4.0.4 on 2022-05-31 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0018_alter_recensioni_stelle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prodotti',
            name='venduti',
            field=models.IntegerField(default=0),
        ),
    ]
