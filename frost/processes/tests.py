from django.test import TestCase

from model_mommy import mommy

from processes.models import Process

from .models import Process


class ProcessModelTests(TestCase):

    def anythingMommy(self):
        anything = mommy.make(Process)
        self.assertTrue(isinstance(anything, Process))
