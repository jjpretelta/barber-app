# Generated by Django 2.1.5 on 2019-07-11 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('berberim', '0012_auto_20190711_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='barbershopemployee',
            name='barbershop',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='barbershop_employees', to='berberim.Barbershop'),
            preserve_default=False,
        ),
    ]
