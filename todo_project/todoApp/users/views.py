from django.shortcuts import render,redirect
import pandas as pd
import datetime
import json
from .models import UserInfo
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
        df = pd.DataFrame(list(UserInfo.objects.filter(first_name='Karthik').filter(completed_task__isnull=True).values()))
        # df = pd.DataFrame(list(UserInfo.objects.all().values('author', 'date', 'slug')))
        print(df.head())
        df.drop(["first_name","completed_task"],inplace=True,axis=1)
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

        if form.is_valid():

            new_author=form.save(commit=False)
            new_author.first_name  = "Karthik"
            new_author.save()
            print("khsdkhdidoodojodojdojoj")

        else:
            print("\n\n\n\n\n it is not valid")
    return redirect('homepage')


def delete_task(request,id):
    print("i am in delete ")
    if request.method == "GET":
        UserInfo.objects.filter(id=id).delete()

    return redirect('homepage')

def completed_task(request,id):
    print("i am in delete ")
    if request.method == "GET":
        import datetime
        # UserInfo.objects.filter(id=id).delete()
        UserInfo.objects.filter(pk=id).update(completed_task=datetime.datetime.now())

    return redirect('homepage')




