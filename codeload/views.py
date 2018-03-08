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
    user = request.user
    if (request.method == 'POST'):
        file = request.FILES['solution']
        solution = models.Solutions(
            task = task,
            created_by = user,
            source = file
        )
        solution.save(force_insert=True)        
        print(solution.source)
        print(task.test_file)
        units = rt.Unit_Test(str(solution.source), str(task.test_file))
        solution.tests_passed = units.run_tests()
        # Here redirect to solutions_view
        return run_solution(request, solution)

def run_solution(request, solution):
    task = solution.task
    print(str(solution.source))
    app = rt.Unit_Test(
        str(solution.source),
        str(task.test_file)
    )
    return HttpResponse(app.run_tests())

def index(request):
    return render(request, 'codeload/index.html')


class TaskListView(generic.ListView):
    model = models.Task
    context_object_name = 'tasks'