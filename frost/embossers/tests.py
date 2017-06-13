from django.test import TestCase

from model_mommy import mommy

from processes.models import Process

from .models import Job, Field


class JobModelTests(TestCase):

    def test_was_created_recently_with_old_job(self):
        """
        was_created_recently() returns False for jobs whose date_created
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        # test_process = mommy.make(Process)
        old_job = mommy.make(Job(date_created=time))
        self.assertIs(old_job.was_created_recently(), False)

    def test_was_created_recently_with_recent_job(self):
        """
        was_created_recently() returns True for jobs whose date_created
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        test_process = mommy.make(Process)
        recent_job = mommy.make(Job(date_created=time))
        self.assertIs(recent_job.was_created_recently(), True)

    def test_was_created_recently_with_future_job(self):
        """
        was_created_recently() returns False for jobs whose date_created
        is in the future
        """
        time = timezone.now() + datetime.timedelta(days=10)
        test_process = mommy.make(Process)
        future_job = mommy.make(Job(date_created=time))
        self.assertIs(future_job.was_created_recently(), False)
