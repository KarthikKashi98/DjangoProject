from django.contrib import admin
# from django.urls import path
from . import views
# from django.conf.urls import url
from django.urls import path, re_path

urlpatterns = [
    # path("admin/", admin.site.urls),
    re_path("todo/", views.home_page, name='homepage'),
    re_path("todo1/", views.home_page1, name='homepage1'),
    re_path("add_task/", views.add_task, name='add_task'),
    re_path(r"delete_task/(?P<id>\d+)/$", views.delete_task, name='delete_task'),
    re_path(r"completed_task/(?P<id>\d+)/$", views.completed_task, name='completed_task'),
    re_path("total_tasks/", views.total_tasks, name='total_task'),
    re_path("completed_tasks/", views.completed_tasks_page, name='completed_tasks_page'),
    re_path("interrupted_tasks/", views.intrupted_tasks_page, name='interrupted_tasks'),
    re_path(r"revert_task/(?P<id>\d+)/$", views.revert_task, name='revert_task'),
    re_path(r"save_edit/", views.save_edit, name='save_edit'),
    re_path(r"update_note/", views.update_note, name='update_note'),
    re_path(r"login/", views.login_page, name='login'),
    re_path(r"signup/", views.signup_page, name='signup'),
    re_path(r"logout/",views.signout,name="logout"),
    re_path(r"dashboard/", views.dashboard, name="dashboard"),
    re_path(r'search/', views.search_person,name="search_person"),
    re_path(r'create_group/', views.create_group, name="create_group"),
    re_path(r'manage_group/get_group/', views.list_of_groups_and_members_in_group, name="get_group"),
    re_path(r'manage_group/delete_group/(?P<id>\d+)/$', views.delete_group, name="delete_group"),
    re_path(r'manage_group/members/(?P<id>\d+)/$', views.get_group_members, name="get_group_members"),
    re_path(r'manage_group/members/delete/(?P<id>\d+)/$', views.delete_member, name="delete_member"),
    re_path(r'manage_group/members/create/', views.add_member_to_the_group, name="add_member_to_the_group"),
    re_path(r'manage_group/add_task_from_group/', views.add_task_from_the_group_manager, name="add_task_from_the_group_manager"),
    re_path(r'manage_group/view_other_group/', views.list_view_other_member_group, name="view_other_group"),

]
