# Generated by Django 2.0.2 on 2018-09-24 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0021_auto_20180914_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='computationalresult',
            name='organism_index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_refinery_common.OrganismIndex'),
        ),
    ]