# Generated by Django 3.2.12 on 2022-04-05 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_buy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buy',
            old_name='product',
            new_name='product_buy',
        ),
        migrations.RenameField(
            model_name='buy',
            old_name='quantity',
            new_name='quantity_prod',
        ),
        migrations.RenameField(
            model_name='buy',
            old_name='user',
            new_name='user_Buying',
        ),
    ]
