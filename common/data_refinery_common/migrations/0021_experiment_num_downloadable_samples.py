# Generated by Django 2.1.8 on 2019-07-01 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0020_update_qn_bucket'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='num_downloadable_samples',
            field=models.IntegerField(default=0),
        ),
    ]
