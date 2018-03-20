from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . import views

@shared_task
def run_solution_task(solution_id):
    solution = views.Solution(solution_id = solution_id)
    solution.run()
    solution.update_leaderboard()