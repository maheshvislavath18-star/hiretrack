from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my/', views.my_applications, name='my_applications'),
    path('update/<int:id>/', views.update_application, name='update_application'),
    path('delete/<int:id>/', views.delete_application, name='delete_application'),

    # ✅ ADD THIS
    path('insert_job/', views.insert_job, name='insert_job'),

    # ✅ NEW (IMPORTANT)
    path('add-job/', views.add_job, name='add_job'),
]