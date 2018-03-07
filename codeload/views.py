from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from . import models
from . import run_tests as rt
import os

# Create your views here.

class TaskDetailView(generic.DetailView):
    model = models.Task
    context_object_name = 'task'

class SolutionsListView(generic.ListView):
    model = models.Solutions
    context_object_name = 'task_solutions_list'
    def get_queryset(self):
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        return task.solutions_set.all()

    
def upload_solution(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id)
    solutions = task.solutions_set
    if (request.method == 'POST'):
        file = request.FILES['solution']
        solution = solutions.create(source=file)
        solution.save()
        return HttpResponseRedirect(reverse('codeload:task', args=(task_id, )))

def run_solution(request, solution_id, in_data):
    solution = get_object_or_404(models.Solutions, pk=solution_id)
    app = rt.App(str(solution.source))
    app.build()
    return HttpResponse(app.run(in_data))