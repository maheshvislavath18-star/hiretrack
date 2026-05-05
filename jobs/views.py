from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication


# 🔥 JOB LIST
@login_required
def job_list(request):
    jobs = Job.objects.all()

    # ✅ get applied job ids for current user
    applied_jobs = JobApplication.objects.filter(
        user=request.user
    ).values_list('job_id', flat=True)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs
    })

# 🔥 APPLY FOR JOB
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # prevent duplicate
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        return HttpResponse("Already Applied ❌")

    JobApplication.objects.create(
        user=request.user,
        job=job,
        status="Applied"
    )

    return redirect('my_applications')


# 🔥 MY APPLICATIONS
@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by('-applied_date')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications   # ✅ IMPORTANT NAME
    })


# 🔥 UPDATE APPLICATION
@login_required
def update_application(request, id):
    application = get_object_or_404(JobApplication, id=id, user=request.user)

    if request.method == "POST":
        application.status = request.POST.get('status')
        application.notes = request.POST.get('notes')
        application.save()
        return redirect('my_applications')

    return render(request, 'jobs/update_application.html', {
        'application': application
    })


# 🔥 DELETE APPLICATION
@login_required
def delete_application(request, id):
    application = get_object_or_404(JobApplication, id=id, user=request.user)

    if request.method == "POST":
        application.delete()
        return redirect('my_applications')

    return render(request, 'jobs/delete_confirm.html', {
        'application': application
    })


# 🔥 TEST DATA
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
    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by('-applied_date')

    total = applications.count()
    applied = applications.filter(status="Applied").count()
    interview = applications.filter(status="Interview").count()
    rejected = applications.filter(status="Rejected").count()

    return render(request, 'jobs/dashboard.html', {
        'applications': applications,
        'total': total,
        'applied': applied,
        'interview': interview,
        'rejected': rejected,
    })

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
        return redirect('job_list')   # go back to job list

    return render(request, 'jobs/add_job.html')