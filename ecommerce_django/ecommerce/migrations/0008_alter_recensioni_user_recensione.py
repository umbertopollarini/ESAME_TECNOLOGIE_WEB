# Generated by Django 4.0.4 on 2022-05-13 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0007_alter_prodotti_fornitore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recensioni',
            name='user_recensione',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]