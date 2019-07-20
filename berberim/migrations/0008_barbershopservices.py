# Generated by Django 2.1.5 on 2019-07-11 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('berberim', '0007_auto_20190707_0344'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarbershopServices',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('price', models.PositiveIntegerField()),
                ('duration_mins', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('barbershop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barbershopservicess', to='berberim.Barbershop')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
