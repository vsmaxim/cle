from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from . import models
from . import run_tests as rt
import os
import json

# Create your views here.

class TaskDetailView(generic.DetailView):
    model = models.Task
    context_object_name = 'task'
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        print(context)
        tests = []
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        # Get first two tests 
        with open(str(task.test_file)) as f:
            count = 0
            for line in f:
                if (count == 2): 
                    break
                count += 1
                tests.append(line.split(','))
        print(tests)                
        context['tests'] = tests
        return context


def show_all_solutions(request):
    solution = models.Solutions.objects.all()[::-1]
    return render(request, 'codeload/all_solutions.html', {
        'solutions': solution,
    })


class SolutionsListView(generic.ListView):
    context_object_name = 'task_solutions_list'
    model = models.Solutions
    def get_queryset(self):
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        return task.solutions_set.all()



class Solution:
    task = None
    user = None
    solution = None
    def __init__(self, task_id, user_id):
        self.task = models.Task.objects.get(pk=task_id)
        self.user = User.objects.get(pk=user_id)
    def set_solution(self, file):
        self.solution = models.Solutions(
            task = self.task,
            created_by = self.user,
            source = file,
        )
        self.solution.save(force_insert=True)
        print(self.solution.source)
        print(self.task)
        unit_tests = rt.Unit_Test(str(self.solution.source), str(self.task.test_file))
        self.solution.tests_passed = unit_tests.run_tests()[1]        
        self.solution.save()
        # self.update_leaderboard()
    def get_solution(self):
        return str(solution)
    def update_leaderboard(self):
        if self.solution and self.solution.tests_passed == -1:
            try: 
                user_solved = self.user.leadership
            except: 
                user_solved = self.user.leadership(
                    user = self.user,
                )
            solved = json.loads(user_solved.solved_string)
            if not self.task.id in solved:
                solved.append(self.task.id)
            user_solved.solved_string = json.dumps(solved)
            user_solved.count_solved = len(solved)
            print(user_solved.solved_string)
            print(user_solved.count_solved)
            user_solved.save()


def upload_solution(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id)
    user = request.user
    if (request.method == 'POST'):
        solution = Solution(task.id, user.id)
        solution.set_solution(request.FILES['solution'])
        # Here redirect to solutions_view
        return redirect('codeload:all_solutions')

def run_solution(request, solution):
    task = solution.task
    print(str(solution.source))
    app = rt.Unit_Test(
        str(solution.source),
        str(task.test_file)
    )
    return HttpResponse(app.run_tests())

def index(request):
    return render(request, 'codeload/base.html')


class TaskListView(generic.ListView):
    model = models.Task
    context_object_name = 'tasks'