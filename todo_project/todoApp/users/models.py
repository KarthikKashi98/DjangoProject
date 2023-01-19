from django.db import models

Status_CHOICES = (
    ('Not_Yet_Started', 'Not_Yet_Started'),
    ('Started', 'Started'),
    ('Interrupted', 'Interrupted'),
    ('Completed', 'Completed'),
)


# Create your models here.
class UserInfo(models.Model):
    first_name = models.CharField(max_length=30,null=True, blank=True)
    date_assigned = models.DateField(auto_now_add=True)
    task_description = models.TextField()
    comments = models.TextField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status_CHOICES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completed_task = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.first_name


# class user_task_note(models.Model):
#     headline = models.CharField(max_length=100)
#     pub_date = models.DateField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.headline
#
#     class Meta:
#         ordering = ['headline']