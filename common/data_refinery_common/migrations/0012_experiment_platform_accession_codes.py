# Generated by Django 2.1.5 on 2019-01-30 21:39

import django.contrib.postgres.fields
from django.db import migrations, models

def update_cached_values(apps, schema_editor):
    """ """

    Experiment = apps.get_model('data_refinery_common', 'Experiment')
    for experiment in Experiment.objects.all():
        # Model methods can't be used during migrations. :(
        # https://stackoverflow.com/a/37685925/1135467
        experiment.platform_accession_codes = list(set([sample.platform_accession_code for sample in experiment.samples.all()]))
        experiment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0011_auto_20190129_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='platform_accession_codes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None),
        ),
        migrations.RunPython(update_cached_values)
    ]