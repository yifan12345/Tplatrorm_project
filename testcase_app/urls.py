from django.urls import path
from testcase_app import views

urlpatterns = [
    # CASE
    path('', views.testcase_manage),
    path('debug/', views.debug),
    path('assert_result/', views.assert_result),
    path('save_case/', views.save_case),

]
