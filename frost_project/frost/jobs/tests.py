import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError

from processes.models import Process

from .models import Job, Field


def create_job(job_id, completed):
    return Job.objects.create(job_id=job_id, completed=completed)

def create_process(process_name):
    return Process.objects.create(process_name=process_name)


class JobModelTests(TestCase):
    def test_was_created_recently_with_old_job(self):
        """
        was_created_recently() returns False for jobs whose date_created
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_job = Job(date_created=time)
        self.assertIs(old_job.was_created_recently(), False)

    def test_was_created_recently_with_recent_job(self):
        """
        was_created_recently() returns True for jobs whose date_created
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_job = Job(date_created=time)
        self.assertIs(recent_job.was_created_recently(), True)

    def test_was_created_recently_with_future_job(self):
        """
        was_created_recently() returns False for jobs whose date_created
        is in the future
        """
        time = timezone.now() + datetime.timedelta(days=10)
        future_job = Job(date_created=time)
        self.assertIs(future_job.was_created_recently(), False)

    def test_two_jobs_with_same_name(self):
        """
        Invalidate a second job using a name already in use
        """
        Job.objects.create(job_id="Job")

        with self.assertRaises(IntegrityError):
            Job.objects.create(job_id="Job")


class JobIndexViewTests(TestCase):
    def test_no_jobs(self):
        """
        if no jobs, exist, display appropriate message.
        """
        response = self.client.get(reverse('jobs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No jobs are available.")
        self.assertQuerysetEqual(response.context['jobs'], [])

    def test_incomplete_job(self):
        """
        if a job is incomplete, it should appear in the incomplete jobs section
        """
        create_job(job_id="Incomplete Job", completed=False)
        response = self.client.get(reverse('jobs:index'))
        self.assertQuerysetEqual(response.context['jobs'], ['<Job: Incomplete Job>'])
        self.assertQuerysetEqual(response.context['incomplete_jobs'], ['<Job: Incomplete Job>'])

    def test_complete_job(self):
        """
        if a job is complete, it should appear in the complete jobs section
        """
        create_job(job_id="Complete Job", completed=True)
        response = self.client.get(reverse('jobs:index'))
        self.assertQuerysetEqual(response.context['jobs'], ['<Job: Complete Job>'])
        self.assertQuerysetEqual(response.context['complete_jobs'], ['<Job: Complete Job>'])


class JobPickTemplateViewTests(TestCase):
    def test_no_templates(self):
        """
        If no templates, the page should say No Templates
        """
        job = create_job(job_id="Test Job", completed=False)
        response = self.client.get(reverse('jobs:pick_template', args=(job.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['processes'], [])
        self.assertContains(response, "No templates available.")

    def test_one_template_named_none(self):
        """
        If only a template named None, the page should show no templates
        """
        job = create_job(job_id="Test Job", completed=False)
        create_process(process_name="None")
        response = self.client.get(reverse('jobs:pick_template', args=(job.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['processes'], ['<Process: None>'])

    def test_one_template_with_name(self):
        """
        If only a template, not named None, the page should show that template
        """
        job = create_job(job_id="Test Job", completed=False)
        create_process(process_name="Template With Name")
        response = self.client.get(reverse('jobs:pick_template', args=(job.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['processes'], ['<Process: Template With Name>'])
        self.assertContains(response, "Template With Name")

    def test_two_templates_one_is_none(self):
        """
        If two templates, one named None, the page should show only named template
        """
        job = create_job(job_id="Test Job", completed=False)
        create_process(process_name="Template With Name")
        create_process(process_name="None")
        response = self.client.get(reverse('jobs:pick_template', args=(job.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "None")
        self.assertContains(response, "Template With Name")

    def test_two_templates_both_named(self):
        """
        If two templates, neither named None, the page should show both templates
        """
        job = create_job(job_id="Test Job", completed=False)
        create_process(process_name="Template With Name 1")
        create_process(process_name="Template With Name 2")
        response = self.client.get(reverse('jobs:pick_template', args=(job.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Template With Name 1")
        self.assertContains(response, "Template With Name 2")
