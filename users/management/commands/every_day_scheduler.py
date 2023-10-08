
from django.core.management.base import BaseCommand
from users.models import UserInfo  # Import the models you want to use
import datetime
import json
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
import sys
sys.path.insert(0, '../todoApp/todoApp')
from django.conf import settings
from django.core.mail import send_mail
# from django.http import HttpResponseRedirectss
# sys.path.insert(0, '../todoApp/users')
# from .models import UserInfo, Main_User_Info, GroupsMembers, GroupInfo


def send_mail_notification(subject, body, to_email):
    print(subject,"\n","body:",body,"\n to email==>",to_email)

    # Construct the email message
    #     subject = "Urgent:Task Completion today"
    #     body = """\
    #     This is an automated reminder regarding the task""" + str(i.id) + """,  As a Reminder,the target date for complete the task by the end of the day
    #     Task Details:
    #     Task Description:"""+i.task_description+"""\n
    #     Thank you for your attention to this matter
    #     Best regards
    #     Your scheduler
    #      """

    from_email = settings.EMAIL_HOST_USER

    # Send the email
    res = send_mail(subject, body, from_email, to_email)
    print(res)
    if (res == 1):
        msg = "Mail Sent Successfuly"

    else:
        msg = "Mail could not sent"
    print(msg)



class Command(BaseCommand):
    help = 'Description of your custom command'

    def handle(self, *args, **options):
        # # Your custom command logic here
        # my_objects = MyModel.objects.all()
        # for obj in my_objects:
        #     self.stdout.write(self.style.SUCCESS(obj.name))
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        user_info = UserInfo.objects.filter(completed_task__isnull=True, target_date__range=(today_min, today_max))
        print(user_info)
        for i in user_info:

            print(i.first_name, "\n", i.first_name.email)
            # Construct the email message
            subject = "Urgent:Task Completion today"
            body = """\
            This is an automated reminder regarding the task""" + str(i.id) + """,  As a Reminder,the target date for complete the task by the end of the day
            Task Details:
            Task Description:"""+i.task_description+"""\n
            Thank you for your attention to this matter
            Best regards 
            Your scheduler
            """

            from_email = settings.EMAIL_HOST_USER
            to_email = [i.first_name.email]

            # Send the email
            res = send_mail(subject, body, from_email, to_email)
            if (res == 1):
                msg = "Mail Sent Successfuly"

            else:
                msg = "Mail could not sent"
            print(msg)


        today_min = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time.max)
        user_info = UserInfo.objects.filter(completed_task__isnull=True, target_date__range=(today_min, today_max))
        for i in user_info:

            print(i.first_name, "\n", i.first_name.email)
            # Construct the email message
            from_email = settings.EMAIL_HOST_USER
            to_email = [i.first_name.email]
            if i.by:
                to_email.append(i.by.group_owner.email)

            subject = "Urgent:Task Completion today"
            body = """\
            This is a friendly reminder that the target completion date for task """+str(i.id)+""" has passed, and the task is still incomplete. As a reminder, completing this task is essential for [Reason for Task], and we would greatly appreciate it if you could complete it as soon as possible.
            Task Details:
            Task Description:"""+i.task_description+"""\n
            Thank you for your attention to this matter
            Best regards 
            Your scheduler
            """
            print(body)



            # Send the email
            res = send_mail(subject, body, from_email, to_email)
            if (res == 1):
                msg = "Mail Sent Successfuly"

            else:
                msg = "Mail could not sent"
            print(msg)

        print("Function executed at specific time every day.")
