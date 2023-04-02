from django.contrib import admin
# from django.urls import path
from . import views
# from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

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
    re_path(r'manage_group/members_task/(?P<id>\d+)/$', views.group_tasks_page, name="view_group_member_task"),
    re_path(r'manage_group/members_total_task/', views.group_member_total_tasks, name="member_total_tasks"),

    re_path(r'manage_group/group_task/(?P<id>\d+)/$', views.total_group_tasks_page, name="total_group_tasks_page"),
    re_path(r'manage_group/group_total_task/', views.group_total_tasks, name="group_total_tasks"),



    re_path('reset_password/',
            auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
            name="reset_password"),
    re_path('reset_password_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html")
            ,name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete'),
]

