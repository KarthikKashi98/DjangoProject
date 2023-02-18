from django.shortcuts import render,redirect,get_object_or_404
import pandas as pd
import datetime
import json
from .models import UserInfo,Main_User_Info
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from .forms import UserInfoForm,CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Count

@login_required(login_url='login')
def home_page(request):
    if request.method == "POST":
        df = pd.DataFrame(list(UserInfo.objects.filter(first_name__username=request.user).values()))
        dtype = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)
        df['priority'] = df.priority.astype(dtype)

        df.sort_values(['priority'], inplace=True, ignore_index=True)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head())
        df.drop(["first_name"],inplace=True)
        # df[""] = None
        df.insert(loc=len(df.columns) - 2,
                  column='',
                  value=None)

        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title":str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        print(my_cols)
        data = {"my_data":my_data,"my_cols":my_cols}
        return data
    context = {}
    initial = {'status': 'Not_Yet_Started'}
    context['form'] = UserInfoForm()
    return render(request,"todo_home_page.html",context)



@csrf_exempt
@login_required(login_url='login')
def home_page1(request):
    print("came to homepage1")
    print(request.user)
    if request.method == "GET":

        # first_name = Main_User_Info.objects.filter(first_name="Karthik")[0].
        # first_name=UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values()
        # q= UserInfo.objects.filter(first_name__first_name=request.user)

        li=list(UserInfo.objects.filter(first_name__username=request.user).filter(completed_task__isnull=True).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(li)
        df.drop(["first_name_id","completed_task"],inplace=True,axis=1)
        df.sort_values(["id"],ascending=False,inplace=True,ignore_index=True)
        df["target_date"]=df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns) - 2,
                  column='',
                  value=None)
        df["date_assigned"]=df["date_assigned"].astype(str)
        dtype = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)
        df['priority'] = df.priority.astype(dtype)

        df.sort_values(['priority'], inplace=True, ignore_index=True)
        print(df.head())
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title":str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data":my_data,"my_cols":my_cols}
        # print(data)
        return JsonResponse(data)


@login_required(login_url='login')
def add_task(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST)
        # print(form)

        # print(Main_User_Info.objects.filter(first_name="Karthik"))

        if form.is_valid():
            new_author=form.save(commit=False)
            new_author.first_name =  request.user #Main_User_Info.objects.filter(first_name="Karthik")[0]

            # new_author.first_name  = "Karthik"
            new_author.save()
            print("khsdkhdidoodojodojdojoj")

        else:
            print("\n\n\n\n\n it is not valid")
    return redirect('homepage')



@login_required(login_url='login')
def delete_task(request,id):
    print("i am in delete ")
    if request.method == "GET":
        UserInfo.objects.filter(id = id).delete()

    return redirect('homepage')


@login_required(login_url='login')
def completed_task(request,id):
    print("i am in delete ")
    if request.method == "GET":
        import datetime
        # UserInfo.objects.filter(id=id).delete()
        # first_name = UserInfo.objects.filter(first_name__first_name='Karthik').filter(
        #     completed_task__isnull=True).values()
        # li = list(
        # UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values())
        q=UserInfo.objects.filter(pk=id)
        if q[0].status == "Interrupted":
            q.update(completed_task=datetime.datetime.now(),status="Interrupted")
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

        UserInfo.objects.filter(pk=id).update(completed_task=None,status="Started")

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
            UserInfo.objects.filter(first_name__username=request.user).filter(~Q(status="Interrupted"),completed_task__isnull=False).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head(1).T)
        df.drop(["first_name_id"], inplace=True, axis=1)
        df["target_date"] = df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns)-2,
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
            UserInfo.objects.filter(first_name__username=request.user).filter(Q(status="Interrupted"),completed_task__isnull=False,).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head(1).T)
        df.drop(["first_name_id"], inplace=True, axis=1)
        df["target_date"] = df["target_date"].astype(str)
        # df[""] = None
        df.insert(loc=len(df.columns)-2,
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
            return JsonResponse({'success':False,"reason":"percentage should be lesser than 100 and grater than 0"})

        UserInfo.objects.filter(pk=id).update(task_description=task_description,
                                              status=status,
                                              target_date = target_date if target_date !="" else None,
                                              percentage = percentage,
                                              priority = priority if priority !="" else None,


                                              )
        return JsonResponse({'success':True})



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
        return JsonResponse({"success":True})

    return redirect('homepage')


@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password= password)
        if user is not None:
            login(request,user)
            print("user is loged in")
            return redirect("homepage")
        else:
            messages.info(request,"username or password is wroung")
            return render(request, "login.html")
    context={}
    return render(request,"login.html",context)


def signup_page(request):
    form = CreateUserForm()

    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request,"Account was created for "+ user)
            return redirect("login")

    context = {"form":form}

    return render(request,"signup.html",context)


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
        print("ijosjos")
        # UserInfo.objects.filter(pk=id).update(completed_task=datetime.datetime.now(), status="Completed",
        #                                       percentage=100)
        # print("------------", UserInfo.objects.filter(~Q(my_field=None)).values("first_name").annotate(Count("first_name")))

        print("=====>",UserInfo.objects.filter(completed_task__isnull=False,status="Interrupted").count(),"<===============")
        q= UserInfo.objects.filter(first_name__username=request.user)
        # print(UserInfo.objects.filter(pk=28)[0].status)
        print("[[[[[[[[[}}}}}}}}}}}}}}}}}",
              q.filter(completed_task__isnull=True).count())

        return JsonResponse({"total_count": q.count(),
                             "completed_task": q.filter(~Q(status="Interrupted"),completed_task__isnull=False,
                                                                               status="Completed").count(),
                             "incomplete_task": q.filter(completed_task__isnull=True).count(),
                             "interrupted_task": q.filter(completed_task__isnull=False,status="Interrupted").count()})

    else:

        print("--------------------------------------------")
        return render(request,"dashboard.html")





@csrf_exempt
def search_person(request):
    """everytime user inputs to search box, this function runs"""
    name = request.GET.get("name")
    namelist = []


    if name:
        #collect every objects that contains the input text

        User = get_user_model()
        # users = User.objects.all()

        # print(users[1].username)
        user_objects = User.objects.filter(username__icontains=name)
        for user in user_objects:
            namelist.append(user.username)
    return JsonResponse({'status':200, 'name':namelist})


