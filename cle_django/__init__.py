from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
import sys

sys.path.insert(0, '/home/vms/Templates')

__all__ = ['celery_app']