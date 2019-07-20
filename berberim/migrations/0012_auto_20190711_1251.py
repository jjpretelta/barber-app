# Generated by Django 2.1.5 on 2019-07-11 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berberim', '0011_auto_20190711_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarbershopEmployee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('title', models.CharField(choices=[('Master', 'Master'), ('Journeyman', 'Journeyman'), ('Apprentice', 'Apprentice')], max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AlterField(
            model_name='barbershopschedule',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
