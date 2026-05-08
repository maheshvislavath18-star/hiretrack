from django.urls import path
from . import views

urlpatterns = [

    # 🔥 JOB LIST
    path(
        '',
        views.job_list,
        name='job_list'
    ),

    # 🔥 DASHBOARD
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # 🔥 APPLY JOB
    path(
        'apply/<int:job_id>/',
        views.apply_job,
        name='apply_job'
    ),

    # 🔥 MY APPLICATIONS
    path(
        'my/',
        views.my_applications,
        name='my_applications'
    ),

    # 🔥 UPDATE APPLICATION
    path(
        'update/<int:id>/',
        views.update_application,
        name='update_application'
    ),

    # 🔥 DELETE APPLICATION
    path(
        'delete/<int:id>/',
        views.delete_application,
        name='delete_application'
    ),

    # 🔥 INSERT TEST JOB
    path(
        'insert_job/',
        views.insert_job,
        name='insert_job'
    ),

    # 🔥 ADD JOB
    path(
        'add-job/',
        views.add_job,
        name='add_job'
    ),

    # 🔥 REST API
    path(
        'api/jobs/',
        views.api_jobs,
        name='api_jobs'
    ),
]