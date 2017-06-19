from django.test import TestCase
from django.db import IntegrityError

from processes.models import Process

from .models import Process


class ProcessModelTests(TestCase):

    def create_process(self):
        new_process = Process()
        self.assertTrue(isinstance(anything, Process))

    def test_two_processes_with_same_name(self):
        """
        Invalidate a second processes using a name already in use
        """
        Process.objects.create(process_name="Process")

        with self.assertRaises(IntegrityError):
            Process.objects.create(process_name="Process")
