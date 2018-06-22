from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from . import models
from . import run_tests as rt
from .tasks import run_solution_task
import json
from . import forms


class TaskDetailView(generic.DetailView, LoginRequiredMixin, FormMixin):
    model = models.Task
    context_object_name = 'task'
    form_class = forms.FileUploadForm

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        with open(str(task.test_file)) as f:
            lines = f.readlines()
            tests = list(map(lambda x: x.split(','), lines[:2]))
        context['tests'] = tests
        return context

    def post(self, request):
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        user = request.user
        solution = Solution(task_id=task.id, user_id=user.id)
        solution.set_solution(request.FILES['solution'])
        run_solution_task.delay(solution.id())
        return redirect('codeload:all_solutions')


class TaskSolutionsListView(generic.ListView, LoginRequiredMixin):
    context_object_name = 'solutions'
    model = models.Solutions
    template_name = 'codeload/solutions.html'

    def get_queryset(self):
        task = get_object_or_404(models.Task, pk=self.kwargs['pk'])
        return task.solutions_set.all()


class AllSolutionsListView(TaskSolutionsListView):
    def get_queryset(self):
        return self.model.objects.all()[::-1]


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
        unit_tests = rt.Unit_Test(str(self.solution.source), str(self.task.test_file))
        self.solution.tests_passed = unit_tests.run_tests()[1]    
        self.solution.running = False    
        self.solution.save()

    def update_leaderboard(self):
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


class SolutionRunner(generic.View, LoginRequiredMixin):

    def get(self, request, solution):
        task = solution.task
        app = rt.Unit_Test(str(solution.source), str(task.test_file))
        return HttpResponse(app.run_tests())


class RatingView(generic.ListView, LoginRequiredMixin):
    context_object_name = 'rate'
    template_name = 'codeload/rating.html'
    model = models.Leadership

    def get_queryset(self):
        return self.model.objects.all()



class TaskListView(generic.ListView, LoginRequiredMixin):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'codeload/task_list.html'