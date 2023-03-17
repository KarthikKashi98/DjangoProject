from django.db import models

from django.contrib.auth.models import User # new

Status_CHOICES = (
    ('Not_Yet_Started', 'Not_Yet_Started'),
    ('Started', 'Started'),
    ('Interrupted', 'Interrupted'),
    ('Completed', 'Completed'),
)


Priority_CHOICES = (
    ('Low', 'Low'),
    ('High', 'High'),
    ('Medium', 'Medium'),

)

Group_role_CHOICES = (
    ('Managerial', 'Managerial'),
    ('Follower', 'Follower'),

)

class Main_User_Info(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return self.first_name



# Create your models here.
class UserInfo(models.Model):
    first_name = models.ForeignKey(User, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)
    # date_assigned = models.DateField()

    task_description = models.TextField()
    comments = models.TextField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status_CHOICES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completed_task = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=Priority_CHOICES,null=True, blank=True)
    # group_name = models.GroupInfo(Main_User_Info, on_delete=models.CASCADE,null=True, blank=True)



    def __str__(self):
        return self.task_description


# Create your models here.
class GroupInfo(models.Model):
    group_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    group_name = models.CharField(
                    max_length = 200,
                    unique = True,null=False, blank=False
                    )
    project_name = models.CharField(
        max_length=200,
        unique=True, null=True, blank=True
    )




    def __str__(self):
        return self.group_owner.username +"(" + self.group_name +")"


class GroupsMembers(models.Model):
    member_name = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.member_name.username +"(" + self.group.group_name +")"
