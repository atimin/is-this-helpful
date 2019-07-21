from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from docsite.models import Site


class DocsiteView(LoginRequiredMixin, TemplateView):
    template_name = 'docsite/docsite_layout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.filter(owner=self.request.user.id)
        return context
