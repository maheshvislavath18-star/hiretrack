from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Job, JobApplication
from .serializers import JobSerializer


# 🔥 HOME PAGE
def home(request):
    return redirect('/accounts/login/')


# 🔥 JOB LIST
@login_required
def job_list(request):
    jobs = Job.objects.all()

    applied_jobs = JobApplication.objects.filter(
        user=request.user
    ).values_list('job_id', flat=True)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs
    })


# 🔥 APPLY JOB
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # prevent duplicate
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        return HttpResponse("Already Applied ❌")

    resume = request.FILES.get('resume')

    JobApplication.objects.create(
        user=request.user,
        job=job,
        status="Applied",
        resume=resume
    )

    return redirect('my_applications')


# 🔥 MY APPLICATIONS
@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by('-applied_date')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })


# 🔥 UPDATE APPLICATION
@login_required
def update_application(request, id):
    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        application.status = request.POST.get('status')
        application.notes = request.POST.get('notes')

        if request.FILES.get('resume'):
            application.resume = request.FILES.get('resume')

        application.save()
        return redirect('my_applications')

    return render(request, 'jobs/update_application.html', {
        'application': application
    })


# 🔥 DELETE APPLICATION
@login_required
def delete_application(request, id):
    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        application.delete()
        return redirect('my_applications')

    return render(request, 'jobs/delete_confirm.html', {
        'application': application
    })


# 🔥 INSERT TEST JOB
def insert_job(request):
    Job.objects.create(
        title="Python Developer",
        company="TCS",
        location="Hyderabad",
        salary="5 LPA",
        description="Django Developer role"
    )

    return HttpResponse("Job Inserted Successfully ✅")


# 🔥 DASHBOARD
@login_required
def dashboard(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by('-applied_date')

    if query:
        applications = applications.filter(
            Q(job__company__icontains=query) |
            Q(job__title__icontains=query)
        )

    if status:
        applications = applications.filter(status=status)

    paginator = Paginator(applications, 5)

    page_number = request.GET.get('page')

    applications = paginator.get_page(page_number)

    total = JobApplication.objects.filter(
        user=request.user
    ).count()

    applied = JobApplication.objects.filter(
        user=request.user,
        status="Applied"
    ).count()

    interview = JobApplication.objects.filter(
        user=request.user,
        status="Interviewing"
    ).count()

    rejected = JobApplication.objects.filter(
        user=request.user,
        status="Rejected"
    ).count()

    return render(request, 'jobs/dashboard.html', {
        'applications': applications,
        'total': total,
        'applied': applied,
        'interview': interview,
        'rejected': rejected,
    })


# 🔥 ADD JOB
@login_required
def add_job(request):

    if request.method == "POST":

        Job.objects.create(
            title=request.POST.get('title'),
            company=request.POST.get('company'),
            location=request.POST.get('location'),
            salary=request.POST.get('salary'),
            description=request.POST.get('description')
        )

        return redirect('job_list')

    return render(request, 'jobs/add_job.html')


# 🔥 API
@api_view(['GET'])
def api_jobs(request):

    jobs = Job.objects.all()

    serializer = JobSerializer(
        jobs,
        many=True
    )

    return Response(serializer.data)