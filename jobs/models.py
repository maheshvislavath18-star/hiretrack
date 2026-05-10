from django.db import models
from django.contrib.auth.models import User


# ✅ Job model
class Job(models.Model):

    title = models.CharField(max_length=100)

    company = models.CharField(max_length=100)

    location = models.CharField(max_length=100)

    salary = models.CharField(max_length=50)

    description = models.TextField()

    def __str__(self):
        return self.title


# ✅ Job Application model
class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_date = models.DateField(
        auto_now_add=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"