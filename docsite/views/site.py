from django.views.generic.edit import CreateView
from docsite.models import Site
from django.urls import reverse_lazy


class SiteCreate(CreateView):
    model = Site
    fields = ['domain_name']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.filter(owner=self.request.user.id)
        return context

