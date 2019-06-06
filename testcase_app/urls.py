from django.urls import path
from testcase_app import views

urlpatterns = [
    # CASE
    path('', views.testcase_manage),
    path('add_case/', views.add_case),
    path('case_edit/<int:cid>/', views.case_edit),
    path('case_delete/', views.case_delete),
    path('debug/', views.debug),
    path('assert_result/', views.assert_result),
    path('save_case/', views.save_case),
    path('get_case_info/', views.get_case_info),

]
