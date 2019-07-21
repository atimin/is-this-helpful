from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class DocsiteView(LoginRequiredMixin, TemplateView):
    template_name = 'docsite/index.html'
