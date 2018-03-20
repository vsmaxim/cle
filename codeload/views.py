from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models
from . import run_tests as rt
from .tasks import run_solution_task
import os
import json

# Create your views here.

class TaskDetailView(generic.DetailView, LoginRequiredMixin):
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

class SolutionsListView(generic.ListView, LoginRequiredMixin):
    context_object_name = 'task_solutions_list'
    model = models.Solutions
    def get_queryset(self):
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        return task.solutions_set.all()

class Solution:
    task = None
    user = None
    solution = None
    def __init__(self, task_id = None , user_id = None, solution_id = None):
        if not task_id is None:
            self.task = models.Task.objects.get(pk=task_id)
            self.user = User.objects.get(pk=user_id)
        elif not solution_id is None:
            self.solution = models.Solutions.objects.get(pk=solution_id)
            self.task = self.solution.task
            self.user = self.solution.created_by
    def set_solution(self, file):
        ''' Creates solution object in database '''
        self.solution = models.Solutions(
            task = self.task,
            created_by = self.user,
            source = file,
            running = True,
        )
        self.solution.save(force_insert=True)
    def id(self):
        return self.solution.id
    def run(self):
        ''' Runs solutions with specified tests for task '''
        unit_tests = rt.Unit_Test(str(self.solution.source), str(self.task.test_file))
        self.solution.tests_passed = unit_tests.run_tests()[1]    
        self.solution.running = False    
        self.solution.save()
    def update_leaderboard(self):
        ''' Updates leaderboard, loads after solution was runned '''
        if self.solution and self.solution.tests_passed == -1:
            try: 
                user_solved = self.user.leadership
            except: 
                user_solved = models.Leadership(
                    user = self.user,
                )
            solved = json.loads(user_solved.solved_string)
            if not self.task.id in solved:
                solved.append(self.task.id)
            user_solved.solved_string = json.dumps(solved)
            user_solved.count_solved = len(solved)
            user_solved.save()

@login_required(redirect_field_name='codeload:index')
def show_all_solutions(request):
    solution = models.Solutions.objects.all()[::-1]
    return render(request, 'codeload/all_solutions.html', {
        'solutions': solution,
    })

@login_required(redirect_field_name='codeload:index')
def upload_solution(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id)
    user = request.user
    if (request.method == 'POST'):
        solution = Solution(task_id = task.id, user_id = user.id)
        solution.set_solution(request.FILES['solution'])
        run_solution_task.delay(solution.id())
        # Here redirect to solutions_view
        return redirect('codeload:all_solutions')

@login_required(redirect_field_name='codeload:index')
def run_solution(request, solution):
    task = solution.task
    print(str(solution.source))
    app = rt.Unit_Test(
        str(solution.source),
        str(task.test_file)
    )
    return HttpResponse(app.run_tests())

def index(request):
    if request.user.is_authenticated:
        return redirect('codeload:tasklist')
    print(request.user.is_authenticated)
    return render(request, 'codeload/base.html')

@login_required(redirect_field_name='codeload:index')
def rating(request):
    rate_list = models.Leadership.objects.all()
    return render(request, 'codeload/rating.html', {
        'rate': rate_list,
    })

class TaskListView(generic.ListView):
    model = models.Task
    context_object_name = 'tasks'