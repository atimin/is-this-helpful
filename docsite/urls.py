from docsite.views import DocsiteView, SiteCreate, post_action, WidgetScripView
from django.urls import path

urlpatterns = [
    path('', DocsiteView.as_view(), name='index'),
    path('sites/create', SiteCreate.as_view(), name='create_site'),
    path('sites/<str:domain_name>/action/new', post_action, name='post_action'),
    path('ith_widget.js', WidgetScripView.as_view(), name='ith_widget')
]
