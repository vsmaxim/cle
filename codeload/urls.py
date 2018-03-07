from django.urls import path
from . import views


app_name = 'codeload'
urlpatterns = [
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task'),
    path('<int:task_id>/upload/', views.upload_solution, name='upload'),
    path('view/<int:pk>/', views.SolutionsListView.as_view(), name='solution'),
    path('run/<int:solution_id>/<str:in_data>/', views.run_solution, name='run_solution'),
]