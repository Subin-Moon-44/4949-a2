# pages/urls.py
from django.urls import path
from .views import homePageView, dataReportView, homePost, results

urlpatterns = [
    path('', homePageView, name='home'),
    path('report/', dataReportView, name='report'),
    path('homePost/', homePost, name="homePost"),
    path('results/<int:age>/<int:weight>/<int:height>/<int:children>/<str:smoker>/', results, name="results"),
]