# Generated by Django 2.2.7 on 2020-01-31 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('berberim', '0018_auto_20200130_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.DeleteModel(
            name='ServiceCategory',
        ),
    ]