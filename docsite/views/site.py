from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import datetime, timedelta
from django.urls import reverse_lazy
from docsite.models import Site,  Action


class SitesLoadedMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.filter(owner=self.request.user.id)
        return context


class SiteCreate(LoginRequiredMixin, SitesLoadedMixin, CreateView):
    model = Site
    fields = ['domain_name']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SiteDetailView(LoginRequiredMixin, SitesLoadedMixin, TemplateView):
    template_name = 'docsite/site_detail.html'

    def get_context_data(self, domain_name, **kwargs):
        context = super().get_context_data(**kwargs)
        site = Site.objects.filter(domain_name=domain_name).first()
        if site:
            docs = []
            for doc in site.document_set.all():
                last_14_days_actions = Action.objects.filter(document_id=doc.id,
                                                             timestamp__lte=datetime.now(),
                                                             timestamp__gte=(datetime.now() - timedelta(14))).all()
                doc.viewed_count = len([a for a in last_14_days_actions if a.action == 'VIEW'])
                doc.helpful_count = len([a for a in last_14_days_actions if a.action == 'HELPFUL'])
                doc.not_helpful_count = len([a for a in last_14_days_actions if a.action == 'NOT_HELPFUL'])
                doc.comments = [a.data for a in last_14_days_actions if a.action == 'NOT_HELPFUL' and a.data]
                doc.doc_raw_size = len(doc.comments) + 1
                docs.append(doc)

        context['docs'] = sorted(docs, key=lambda d: d.viewed_count, reverse=True)

        return context
