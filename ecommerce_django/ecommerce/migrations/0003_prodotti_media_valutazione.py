# Generated by Django 4.0.4 on 2022-05-04 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_acquirenti_remove_recensioni_id_user_recensione_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prodotti',
            name='media_valutazione',
            field=models.IntegerField(default=0),
        ),
    ]
