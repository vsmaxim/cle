from django.urls import path
from . import views


app_name = 'codeload'
urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasklist'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task'),
    path('view/<int:pk>/', views.TaskSolutionsListView.as_view(), name='solution'),
    path('run/<int:solution_id>/<str:in_data>/', views.SolutionRunner.as_view(), name='run_solution'),
    path('solutionslist/', views.AllSolutionsListView.as_view(), name='all_solutions'),
    path('rating/', views.RatingView.as_view(), name='rating')
]