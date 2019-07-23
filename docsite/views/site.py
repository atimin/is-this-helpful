"""
   Copyright 2019 Aleksey Timin

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import datetime, timedelta
from django.urls import reverse_lazy
from docsite.models import Site, Action


class SitesLoadedMixin(ContextMixin):                                           # pylint: disable=too-few-public-methods
    """Mixin to load all the sites"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.filter(owner=self.request.user.id)
        return context


class SiteCreate(LoginRequiredMixin, SitesLoadedMixin, CreateView):             # pylint: disable=too-many-ancestors
    """Creates a new site """

    model = Site
    fields = ['domain_name']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SiteDetailView(LoginRequiredMixin, SitesLoadedMixin, TemplateView):       # pylint: disable=too-many-ancestors
    """Shows site page with statistics"""

    template_name = 'docsite/site_detail.html'

    def get_context_data(self, domain_name, **kwargs):                          # pylint: disable=arguments-differ
        context = super().get_context_data(**kwargs)
        site = Site.objects.filter(domain_name=domain_name).first()
        if site:
            docs = []
            for doc in site.document_set.all():
                now = datetime.now()
                two_weeks_before = (now - timedelta(14))
                last_14_days_actions = Action.objects.filter(document_id=doc.id,
                                                             timestamp__lte=now,
                                                             timestamp__gte=two_weeks_before).all()
                doc.viewed_count = len([a for a in last_14_days_actions if a.action == 'VIEW'])
                doc.helpful_count = len([a for a in last_14_days_actions if a.action == 'HELPFUL'])
                doc.not_helpful_count = len([a for a in last_14_days_actions
                                             if a.action == 'NOT_HELPFUL'])
                doc.comments = [a.data for a in last_14_days_actions
                                if a.action == 'NOT_HELPFUL' and a.data]
                doc.doc_raw_size = len(doc.comments) + 1
                docs.append(doc)

        context['docs'] = sorted(docs, key=lambda d: d.viewed_count, reverse=True)

        return context
