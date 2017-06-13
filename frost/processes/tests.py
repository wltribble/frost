from django.test import TestCase

from processes.models import Process

from .models import Process


class ProcessModelTests(TestCase):

    def create_process(self):
        new_process = Process()
        self.assertTrue(isinstance(anything, Process))
