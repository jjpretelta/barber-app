# Generated by Django 2.1.5 on 2019-06-30 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berberim', '0002_auto_20190630_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertype',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
