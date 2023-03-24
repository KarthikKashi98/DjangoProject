from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
import datetime
import json
from .models import UserInfo, Main_User_Info, GroupsMembers, GroupInfo
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from .forms import UserInfoForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import sys

sys.path.insert(0, '../todoApp/todoApp')
from django.conf import settings
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit


def my_function():
    # Do something
    name = "kk"
    email = "karthik4gmit@gmail.com"
    message = "om........"
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
        print(body)
        from_email = settings.EMAIL_HOST_USER
        to_email = [i.first_name.email]

        # Send the email
        res = send_mail(subject, body, from_email, to_email)
        if (res == 1):
            msg = "Mail Sent Successfuly"

        else:
            msg = "Mail could not sent"
        print(msg)
    # return HttpResponse(msg)
    print("Function executed at specific time every day.")


scheduler = BackgroundScheduler()
scheduler.add_job(my_function, trigger=CronTrigger(year="*", day="*", hour=0, minute=0))
scheduler.start()


def on_exit():
    scheduler.shutdown()


atexit.register(on_exit)


@login_required(login_url='login')
def home_page(request):
    if request.method == "POST":
        df = pd.DataFrame(list(UserInfo.objects.filter(first_name__username=request.user).values()))
        dtype = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)
        df['priority'] = df.priority.astype(dtype)

        df.sort_values(['priority'], inplace=True, ignore_index=True)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head())
        df.drop(["first_name"], inplace=True)
        # df[""] = None
        df.insert(loc=len(df.columns) - 2,
                  column='',
                  value=None)

        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        return data
    context = {}
    initial = {'status': 'Not_Yet_Started'}
    context['form'] = UserInfoForm()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    user_info = UserInfo.objects.filter(completed_task__isnull=True, target_date__range=(today_min, today_max))
    print(user_info)
    for i in user_info:
        print(i.first_name, "\n", i.first_name.email)
    return render(request, "todo_home_page.html", context)


@csrf_exempt
@login_required(login_url='login')
def home_page1(request):
    print("came to homepage1")
    print(request.user)
    if request.method == "GET":
        # first_name = Main_User_Info.objects.filter(first_name="Karthik")[0].
        # first_name=UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values()
        # q= UserInfo.objects.filter(first_name__first_name=request.user)

        li = list(
            UserInfo.objects.filter(first_name__username=request.user).filter(completed_task__isnull=True).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(li)
        df.drop(["first_name_id", "completed_task"], inplace=True, axis=1)
        df.sort_values(["id"], ascending=False, inplace=True, ignore_index=True)
        df["target_date"] = df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns) - 2,
                  column='',
                  value=None)
        df["date_assigned"] = df["date_assigned"].astype(str)
        dtype = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)
        df['priority'] = df.priority.astype(dtype)

        df.sort_values(['priority'], inplace=True, ignore_index=True)
        print(df.head())
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        # print(data)
        return JsonResponse(data)


@login_required(login_url='login')
def add_task(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST)
        # print(form)

        # print(Main_User_Info.objects.filter(first_name="Karthik"))

        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.first_name = request.user  # Main_User_Info.objects.filter(first_name="Karthik")[0]

            # new_author.first_name  = "Karthik"
            new_author.save()
            print("khsdkhdidoodojodojdojoj")

        else:
            print("lalalalalalal")
            print("\n\n\n\n\n it is not valid")
    return redirect('homepage')


@login_required(login_url='login')
def delete_task(request, id):
    print("i am in delete ")
    if request.method == "GET":
        UserInfo.objects.filter(id=id).delete()

    return redirect('homepage')


@login_required(login_url='login')
def completed_task(request, id):
    print("i am in delete ")
    if request.method == "GET":
        import datetime
        # UserInfo.objects.filter(id=id).delete()
        # first_name = UserInfo.objects.filter(first_name__first_name='Karthik').filter(
        #     completed_task__isnull=True).values()
        # li = list(
        # UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values())
        q = UserInfo.objects.filter(pk=id)
        if q[0].status == "Interrupted":
            q.update(completed_task=datetime.datetime.now(), status="Interrupted")
        else:
            q.update(completed_task=datetime.datetime.now(), status="Completed", percentage=100)
        # UserInfo.objects.filter(pk=28)[0].status

    return redirect('homepage')


@csrf_exempt
@login_required(login_url='login')
def total_tasks(request):
    print("i am in total_task ")
    if request.method == "GET":
        return render(request, "total_task.html")

    if request.method == "POST":
        print("i am in total task")
        li = list(
            UserInfo.objects.filter(first_name__username=request.user).values())
        df = pd.DataFrame(li)
        df.drop(["first_name_id", "completed_task"], inplace=True, axis=1)

        df["target_date"] = df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns) - 1,
                  column='',
                  value=None)
        df["date_assigned"] = df["date_assigned"].astype(str)
        print(df.head(1).T)
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        # print(data)
        return JsonResponse(data)


@login_required(login_url='login')
def revert_task(request, id):
    print("i am in delete ")
    if request.method == "GET":
        import datetime

        UserInfo.objects.filter(pk=id).update(completed_task=None, status="Started")

    return redirect('homepage')


@csrf_exempt
@login_required(login_url='login')
def completed_tasks_page(request):
    print("i am in completed---------_task ")
    if request.method == "GET":
        return render(request, "completed_task.html")

    if request.method == "POST":
        print("i am in completed---------_task ")
        li = list(
            UserInfo.objects.filter(first_name__username=request.user).filter(~Q(status="Interrupted"),
                                                                              completed_task__isnull=False).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head(1).T)
        df.drop(["first_name_id"], inplace=True, axis=1)
        df["target_date"] = df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns) - 2,
                  column='',
                  value=None)
        df["date_assigned"] = df["date_assigned"].astype(str)
        df["completed_task"] = df["completed_task"].astype(str)
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        # print(data)
        return JsonResponse(data)


@csrf_exempt
@login_required(login_url='login')
def intrupted_tasks_page(request):
    print("i am in completed---------_task ")
    if request.method == "GET":
        return render(request, "intrupted_task.html")

    if request.method == "POST":
        print("i am in intrupted---------_task ")
        li = list(
            UserInfo.objects.filter(first_name__username=request.user).filter(Q(status="Interrupted"),
                                                                              completed_task__isnull=False, ).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head(1).T)
        df.drop(["first_name_id"], inplace=True, axis=1)
        df["target_date"] = df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns) - 2,
                  column='',
                  value=None)
        df["date_assigned"] = df["date_assigned"].astype(str)
        df["completed_task"] = df["completed_task"].astype(str)
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        # print(data)
        return JsonResponse(data)


@csrf_exempt
@login_required(login_url='login')
def save_edit(request):
    if request.method == "POST":
        print("\n\n\n\nheloooooooooooo i am here.................")

        updatedData = json.loads(request.body.decode('UTF-8'))
        print(updatedData)
        status = updatedData["status"]
        task_description = updatedData["task_description"]
        target_date = updatedData["target_date"]
        percentage = updatedData["percentage"]
        priority = updatedData["priority"]
        id = updatedData["id"]

        if int(percentage) > 100 or int(percentage) < 0:
            return JsonResponse({'success': False, "reason": "percentage should be lesser than 100 and grater than 0"})

        UserInfo.objects.filter(pk=id).update(task_description=task_description,
                                              status=status,
                                              target_date=target_date if target_date != "" else None,
                                              percentage=percentage,
                                              priority=priority if priority != "" else None,

                                              )
        return JsonResponse({'success': True})


@csrf_exempt
@login_required(login_url='login')
def update_note(request):
    print("i am in get note ")
    if request.method == "POST":
        print("=========================")
        updatedData = json.loads(request.body.decode('UTF-8'))
        note = updatedData["note"]
        id = int(updatedData["id"])
        UserInfo.objects.filter(pk=id).update(note=note)
        return JsonResponse({"success": True})

    return redirect('homepage')


@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("user is loged in")
            return redirect("homepage")
        else:
            messages.info(request, "username or password is wroung")
            return render(request, "login.html")
    context = {}
    return render(request, "login.html", context)


def signup_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("login")

    context = {"form": form}

    return render(request, "signup.html", context)


@login_required(login_url='login')
def signout(request):
    try:

        logout(request)
    except Exception as e:
        print(e)
    return redirect("login")


@csrf_exempt
@login_required(login_url='login')
def dashboard(request):
    if request.method == "POST":

        print("=====>", UserInfo.objects.filter(completed_task__isnull=False, status="Interrupted").count(),
              "<===============")
        q = UserInfo.objects.filter(first_name__username=request.user)
        # print(UserInfo.objects.filter(pk=28)[0].status)
        print("[[[[[[[[[}}}}}}}}}}}}}}}}}",
              q.filter(completed_task__isnull=True).count())

        return JsonResponse({"total_count": q.count(),
                             "completed_task": q.filter(~Q(status="Interrupted"), completed_task__isnull=False,
                                                        status="Completed").count(),
                             "incomplete_task": q.filter(completed_task__isnull=True).count(),
                             "interrupted_task": q.filter(completed_task__isnull=False, status="Interrupted").count()})

    else:

        print("--------------------------------------------")
        context = {}
        context["category"] = "create_group"
        return render(request, "dashboard.html", context)


@csrf_exempt
def search_person(request):
    """everytime user inputs to search box, this function runs"""
    name = request.GET.get("name")
    namelist = []

    if name:
        # collect every objects that contains the input text

        User = get_user_model()
        # users = User.objects.all()

        # print(users[1].username)
        user_objects = User.objects.filter(username__icontains=name)
        for user in user_objects:
            namelist.append(user.username)
    return JsonResponse({'status': 200, 'name': namelist})


@csrf_exempt
@login_required(login_url='login')
# @transaction.atomic
def create_group(request):
    if request.method == "POST":

        group_data = json.loads(request.body.decode('UTF-8'))
        group_members = group_data["list_group_member"]
        group_name = group_data["group_name"]
        # q = UserInfo.objects.filter(first_name__username=)
        group = GroupInfo(group_owner=request.user, group_name=group_name)
        group.save()
        # sid = transaction.savepoint()
        #
        # transaction.savepoint_commit(sid)
        User = get_user_model()
        print("\n\n\n\n\n\ngroup_members=========>", group_members, "=======\n\n\n\n\n\n")
        if request.user.username not in group_members:
            group_member = GroupsMembers(group=group, member_name=request.user)
            group_member.save()

        for i in group_members:
            user_objects = User.objects.filter(username=i)[0]
            group_member = GroupsMembers(group=group, member_name=user_objects)
            group_member.save()

        return JsonResponse({"success": True})


@csrf_exempt
@login_required(login_url='login')
# @transaction.atomic
def list_of_groups_and_members_in_group(request):
    if request.method == "GET":
        group_info = GroupInfo.objects.filter(group_owner=request.user)
        print(group_info.values())
        groups_members = GroupsMembers.objects.filter(group__group_owner=request.user)
        print("group_info==>", list(group_info.values()))
        print("group_members==>", list(groups_members.values()))
        group_info = list(group_info.values())
        group_members = groups_members
        for i in range(len(group_info)):
            for j in range(len(group_members)):
                if group_info[i]["id"] == group_members[j].group_id:
                    group_info[i]["members"] = group_info[i].get("members", []) + [
                        group_members[j].member_name.username]
                    # print(group_members[j].group_id)
                    #
                    # print(group_members[j].member_name)
                group_info[i]["members"] = group_info[i].get("members", [])
        print("--=group_info========>", {"group_info": group_info})

        return JsonResponse({"group_info": group_info})


@csrf_exempt
@login_required(login_url='login')
def delete_group(request, id):
    print("i am villain............")

    GroupInfo.objects.filter(id=id).delete()
    return redirect('dashboard')


@csrf_exempt
@login_required(login_url='login')
def delete_member(request, id):
    print("i am villain............")

    GroupsMembers.objects.filter(id=id).delete()
    return redirect('dashboard')


@csrf_exempt
@login_required(login_url='login')
# @transaction.atomic
def get_group_members(request, id):
    if request.method == "GET":
        group_members = GroupsMembers.objects.filter(group__id=id)

        group_members_list = []
        for i in range(len(group_members)):
            temp_dict = {"id": group_members[i].id}
            temp_dict["joined_date"] = group_members[i].joined_date

            temp_dict["member_name"] = group_members[i].member_name.username
            temp_dict["designation"] = "Member" if group_members[i].member_name.username != group_members[
                i].group.group_owner.username else "Instigator"

            group_members_list.append(temp_dict)

        print(group_members_list)

        print("group_info==>", list(group_members.values()))
        if len(list(group_members.values())):

            print("group_members========>",
                  {"group_id": group_members[0].group_id, "group_name": group_members[0].group.group_name,
                   "group_members": group_members_list})

            return JsonResponse(
                {"group_id": id, "group_name": group_members[0].group.group_name, "group_members": group_members_list})

        else:

            return JsonResponse({"group_id": id, "group_name": "no members in the group", "group_members": []})


@csrf_exempt
@login_required(login_url='login')
# @transaction.atomic
def add_member_to_the_group(request):
    print("\n\n\n\n i am in add memner group")
    member_data = json.loads(request.body.decode('UTF-8'))
    group_id = int(member_data["group_id"])
    print("group_id===========>", group_id, type(group_id))
    member_name = member_data["username"]
    User = get_user_model()
    user_objects = User.objects.filter(username__icontains=member_name)[0]
    group_object = GroupInfo.objects.filter(id=group_id)[0]
    print(group_object)
    group_member = GroupsMembers(group=group_object, member_name=user_objects)
    group_member.save()

    return JsonResponse({"success": True})


@login_required(login_url='login')
def add_task_from_the_group_manager(request):
    print("\n\n\n\nheloooooooooooo i am here.................")
    if request.method == "POST":

        print("\n\n\n\nheloooooooooooo i am here.................")

        json_string = request.body.decode('utf-8')
        add_task = json.loads(json_string)
        # print(add_task.task1)

        task = add_task["task1"]
        comments = add_task["comments1"]
        note = add_task["note1"]
        target_date = add_task["target_date1"]
        priority = add_task["priority1"]
        status = add_task["status1"]
        group_name = add_task["group_name1"]
        member_name = add_task["member_name1"]

        print("\n", add_task, "\n")

        print("success")
        try:
            User = get_user_model()
            user_objects = User.objects.filter(username=member_name)[0]
            print(task)
            initial_values = {

                'task_description': task,
                'comments': comments,
                'target_date': target_date,
                'status': status,
                'note': note,
                'priority': priority
            }
            form = UserInfoForm(data=initial_values)

            print(user_objects)

            if form.is_valid():
                new_author = form.save(commit=False)
                new_author.first_name = user_objects  # Main_User_Info.objects.filter(first_name="Karthik")[0]

                # new_author.first_name  = "Karthik"
                new_author.save()
                print("kjlkklskkksokosdkokdok")
            # form.save(comit=True)

            else:
                print(form.errors)
                print("form is invalid")
                return JsonResponse({"success": False, "reason": "please try again later"})

            # print("khsdkhdidoodojodojdojoj")

            return JsonResponse({"success": True})

        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "reason": "please try again later"})


@csrf_exempt
@login_required(login_url='login')
# @transaction.atomic
def list_view_other_member_group(request):
    if request.method == "GET":
        group_name = GroupsMembers.objects.filter(~Q(group__group_owner=request.user) & Q(member_name=request.user))
        print(group_name)
        group_info = []
        for i in group_name:
            a = GroupsMembers.objects.aggregate(

                c1=Count('pk', filter=Q(group__group_name=i.group.group_name))
            )
            dict_group_info = {}
            dict_group_info["group_name"] = i.group.group_name
            dict_group_info["id"] = i.group.id
            dict_group_info["count_members"] = a["c1"]
            group_info.append(dict_group_info)

        return JsonResponse({"group_info": group_info})
