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
from .forms import UserInfoForm

def home_page(request):
    if request.method == "POST":
        df = pd.DataFrame(list(UserInfo.objects.filter(first_name='karthik').values()))
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head())
        df.drop(["first_name"],inplace=True)
        df[""]=None

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
def home_page1(request):
    print("came to homepage1")
    if request.method == "GET":
        # first_name = Main_User_Info.objects.filter(first_name="Karthik")[0].
        first_name=UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values()
        li=list(UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values())
        df = pd.DataFrame(li)
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(li)
        df.drop(["first_name_id","completed_task"],inplace=True,axis=1)
        df["target_date"]=df["target_date"].astype(str)
        df[""] = None
        df["date_assigned"]=df["date_assigned"].astype(str)
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title":str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data":my_data,"my_cols":my_cols}
        # print(data)
        return JsonResponse(data)



def add_task(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST)
        # print(form)

        print(Main_User_Info.objects.filter(first_name="Karthik"))

        if form.is_valid():
            new_author=form.save(commit=False)
            new_author.first_name =  Main_User_Info.objects.filter(first_name="Karthik")[0]

            # new_author.first_name  = "Karthik"
            new_author.save()
            print("khsdkhdidoodojodojdojoj")

        else:
            print("\n\n\n\n\n it is not valid")
    return redirect('homepage')


def delete_task(request,id):
    print("i am in delete ")
    if request.method == "GET":
        UserInfo.objects.filter().delete()

    return redirect('homepage')

def completed_task(request,id):
    print("i am in delete ")
    if request.method == "GET":
        import datetime
        # UserInfo.objects.filter(id=id).delete()
        # first_name = UserInfo.objects.filter(first_name__first_name='Karthik').filter(
        #     completed_task__isnull=True).values()
        # li = list(
        # UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=True).values())

        UserInfo.objects.filter(pk=id).update(completed_task=datetime.datetime.now(),status="Completed",percentage= 100)

    return redirect('homepage')







@csrf_exempt
def total_tasks(request):
    print("i am in total_task ")
    if request.method == "GET":

        return render(request, "total_task.html")

    if request.method == "POST":
        li = list(
            UserInfo.objects.filter(first_name__first_name='Karthik').values())
        df = pd.DataFrame(li)
        df.drop(["first_name_id", "completed_task"], inplace=True, axis=1)
        df["target_date"] = df["target_date"].astype(str)
        df[""] = None
        df["date_assigned"] = df["date_assigned"].astype(str)
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        # print(data)
        return JsonResponse(data)


def revert_task(request, id):
    print("i am in delete ")
    if request.method == "GET":
        import datetime

        UserInfo.objects.filter(pk=id).update(completed_task=None,status="Started")

    return redirect('homepage')



@csrf_exempt
def completed_tasks_page(request):
    print("i am in completed---------_task ")
    if request.method == "GET":

        return render(request, "completed_task.html")

    if request.method == "POST":
        print("i am in completed---------_task ")
        li = list(
            UserInfo.objects.filter(first_name__first_name='Karthik').filter(completed_task__isnull=False).values())
        df = pd.DataFrame(li)
                # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head(1).T)
        df.drop(["first_name_id"], inplace=True, axis=1)
        df["target_date"] = df["target_date"].astype(str)
        df[""] = None
        df["date_assigned"] = df["date_assigned"].astype(str)
        df["completed_task"] = df["completed_task"].astype(str)
        my_data = json.loads(df.to_json(orient="split"))["data"]
        my_cols = [{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]]
        # print(my_cols)
        data = {"my_data": my_data, "my_cols": my_cols}
        # print(data)
        return JsonResponse(data)



@csrf_exempt
def save_edit(request):
    if request.method == "POST":
        print("\n\n\n\nheloooooooooooo i am here.................")

        updatedData = json.loads(request.body.decode('UTF-8'))
        print(updatedData)
        status = updatedData["status"]
        task_description = updatedData["task_description"]
        target_date = updatedData["target_date"]
        percentage = updatedData["percentage"]
        id = updatedData["id"]

        if int(percentage) > 100 or int(percentage) < 0:
            return JsonResponse({'success':False,"reason":"percentage should be lesser than 100 and grater than 0"})

        UserInfo.objects.filter(pk=id).update(task_description=task_description,
                                              status=status,
                                              target_date = target_date if target_date !="" else None,
                                              percentage = percentage


                                              )
        return JsonResponse({'success':True})



@csrf_exempt
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