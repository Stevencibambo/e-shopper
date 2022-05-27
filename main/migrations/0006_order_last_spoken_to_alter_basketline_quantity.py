# Generated by Django 4.0.4 on 2022-05-23 03:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='last_spoken_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cs_chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='basketline',
            name='quantity',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
