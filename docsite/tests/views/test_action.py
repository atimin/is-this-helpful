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

import json
from django.test import TestCase
from docsite.models import Document


class TestAction(TestCase):
    """Action View Test"""

    fixtures = ['base.yaml']

    def setUp(self) -> None:
        self.view_payload = json.dumps({
            'path': '/doc/help1.html',
            'action': 'VIEW'
        })

    def test_site_not_found(self):
        """Action View should return error 404 if the site is not found"""

        request = self.client.post('/sites/www.NOTFOUND.org/action/new',
                                   self.view_payload,
                                   content_type='application/json')
        self.assertEqual(404, request.status_code)

    def test_wrong_method(self):
        """Action View should return error 405 if method is wrong"""

        request = self.client.get('/sites/www.site.org/action/new')
        self.assertEqual(405, request.status_code)

    def test_wrong_payload(self):
        """Action View should return error 422 if the JSON format is wrong"""

        wrong_payload = json.dumps({
            'path': '/doc/help1.html',
            'action': 'UNSUPPORTED_ACTION'
        })

        request = self.client.post('/sites/www.site.org/action/new',
                                   wrong_payload,
                                   content_type='application/json')
        self.assertEqual(422, request.status_code)

    def test_create_doc_at_first_action(self):
        """Action View should create a document if it doesn't exist"""

        payload = json.dumps({
            'path': '/doc/help2.html',
            'action': 'VIEW'
        })

        request = self.client.post('/sites/www.site.org/action/new',
                                   payload,
                                   content_type='application/json')

        self.assertEqual(200, request.status_code)

        doc = Document.objects.filter(path='/doc/help2.html').first()
        self.assertIsNotNone(doc)

    def test_view_action(self):
        """Action View should record 'VIEW' action"""
        request = self.client.post('/sites/www.site.org/action/new',
                                   self.view_payload,
                                   content_type='application/json')

        self.assertEqual(200, request.status_code)

        doc: Document = Document.objects.filter(pk=1).first()
        self.assertEqual(1, doc.action_set.count())
        self.assertEqual('VIEW', doc.action_set.first().action)
