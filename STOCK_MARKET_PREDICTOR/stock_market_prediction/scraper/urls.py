from django.urls import path
from .views import scrape_and_return_data

urlpatterns = [
    path('scrape/', scrape_and_return_data, name='scrape_and_return_data'),
]
