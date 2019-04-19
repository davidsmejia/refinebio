"""This command will create and run survey jobs for each experiment
in the experiment_list. experiment list should be a file containing
one experiment accession code per line.
"""

import boto3
import botocore
import nomad
import uuid

from django.core.management.base import BaseCommand
from nomad.api.exceptions import URLNotFoundNomadException

from data_refinery_common.logging import get_and_configure_logger
from data_refinery_common.job_lookup import SurveyJobTypes
from data_refinery_common.message_queue import send_job
from data_refinery_common.models import SurveyJob, SurveyJobKeyValue
from data_refinery_common.utils import parse_s3_url, get_env_variable
from data_refinery_foreman.surveyor import surveyor

from data_refinery_common.models import (
    ComputationalResult,
    ComputedFile,
    Dataset,
    Experiment,
    ExperimentOrganismAssociation,
    ExperimentSampleAssociation,
    ExperimentSampleAssociation,
    Organism,
    OrganismIndex,
    ProcessorJob,
    ProcessorJobDatasetAssociation,
    Sample,
    SampleComputedFileAssociation,
)
from data_refinery_workers.processors import qn_reference, utils

logger = get_and_configure_logger(__name__)

MIN = 100

class Command(BaseCommand):

    def handle(self, *args, **options):
        """ Handle it! """

        organisms = Organism.objects.all()

        for organism in organisms:
            samples = Sample.processed_objects.filter(organism=organism, has_raw=True, technology="MICROARRAY", is_processed=True)
            if samples.count() < MIN:
                logger.error("Proccessed samples don't meet minimum threshhold",
                    organism=organism,
                    count=samples.count(),
                    min=MIN
                )
                continue

            platform_counts = samples.values('platform_accession_code').annotate(dcount=Count('platform_accession_code')).order_by('-dcount')
            biggest_platform = platform_counts[0]['platform_accession_code']

            sample_codes_results = Sample.processed_objects.filter(
                platform_accession_code=biggest_platform,
                has_raw=True,
                technology="MICROARRAY",
                organism=organism,
                is_processed=True).values('accession_code')
            sample_codes = [res['accession_code'] for res in sample_codes_results]

            dataset = Dataset()
            dataset.data = {organism.name + '_(' + biggest_platform + ')': sample_codes}
            dataset.aggregate_by = "ALL"
            dataset.scale_by = "NONE"
            dataset.quantile_normalize = False
            dataset.save()

            job = ProcessorJob()
            job.pipeline_applied = "QN_REFERENCE"
            job.save()

            pjda = ProcessorJobDatasetAssociation()
            pjda.processor_job = job
            pjda.dataset = dataset
            pjda.save()

            logger.info("Sending QN_REFERENCE for Organism", job_id=str(job.pk), organism=str(organism))
            send_job(ProcessorPipeline.QN_REFERENCE, processor_job)