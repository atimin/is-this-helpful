from docsite.views import DocsiteView, SiteCreate
from django.urls import path

urlpatterns = [
    path('', DocsiteView.as_view(), name='index'),
    path('sites/create', SiteCreate.as_view(), name='create_site')
]
