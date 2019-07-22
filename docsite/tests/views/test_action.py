import json
from django.test import TestCase
from docsite.models import Document


class TestAction(TestCase):

    fixtures = ['base.yaml']

    def setUp(self) -> None:
        self.view_payload = json.dumps({
            'path': '/doc/help1.html',
            'action': 'VIEW'
        })

    def test_site_not_found(self):
        request = self.client.post('/sites/www.NOTFOUND.org/action/new',
                                   self.view_payload,
                                   content_type='application/json')
        self.assertTrue(404, request.status_code)

    def test_wrong_content_type(self):
        request = self.client.post('/sites/www.site.org/action/new')
        self.assertTrue(415, request.status_code)

    def test_wrong_method(self):
        request = self.client.get('/sites/www.site.org/action/new')
        self.assertTrue(405, request.status_code)

    def test_wrong_payload(self):
        wrong_payload = json.dumps({
            'path': '/doc/help1.html',
            'action': 'UNSUPPORTED_ACTION'
        })

        request = self.client.post('/sites/www.site.org/action/new',
                                   wrong_payload,
                                   content_type='application/json')
        self.assertTrue(422, request.status_code)

    def test_create_doc_at_first_action(self):
        payload = json.dumps({
            'path': '/doc/help2.html',
            'action': 'VIEW'
        })

        request = self.client.post('/sites/www.site.org/action/new',
                                   payload,
                                   content_type='application/json')

        self.assertTrue(200, request.status_code)

        doc = Document.objects.filter(path='/doc/help2.html').first()
        self.assertIsNotNone(doc)

    def test_view_action(self):
        request = self.client.post('/sites/www.site.org/action/new',
                                   self.view_payload,
                                   content_type='application/json')

        self.assertTrue(200, request.status_code)
        doc: Document = Document.objects.filter(pk=1).first()
        self.assertEqual(1, doc.action_set.count())
