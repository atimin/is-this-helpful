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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from docsite.models import Site


class DocsiteView(LoginRequiredMixin, TemplateView):
    """Main page"""

    template_name = 'docsite/docsite_layout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.filter(owner=self.request.user.id)
        return context


class WidgetScripView(TemplateView):
    """Provides the script with widget code"""

    template_name = 'docsite/ith_widget.js'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        context['hostname'] = request.get_host()
        return self.render_to_response(context)
