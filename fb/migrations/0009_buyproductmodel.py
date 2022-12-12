# Generated by Django 4.1.3 on 2022-12-07 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fb', '0008_alter_uploadvideosmodel_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('Card_number', models.DecimalField(decimal_places=10, max_digits=12)),
                ('CVV', models.DecimalField(decimal_places=3, max_digits=4)),
                ('Phone_number', models.DecimalField(decimal_places=10, max_digits=12)),
                ('Address', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
