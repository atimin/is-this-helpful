from docsite.views import DocsiteView, SiteCreate, post_action
from django.urls import path

urlpatterns = [
    path('', DocsiteView.as_view(), name='index'),
    path('sites/create', SiteCreate.as_view(), name='create_site'),
    path('sites/<str:domain_name>/action/new', post_action, name='post_action')
]
