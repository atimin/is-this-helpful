import json
from schema import Schema, And, Use, Optional
from docsite.models import Site, Action
from django.http import HttpResponse

ACTION_PAYLOAD_SCHEMA = Schema(
    {
        'path': And(str),
        'action': And(Use(str), lambda a: a in ['VIEW', 'HELPFUL', 'NOT_HELPFUL']),
        Optional('data'): And(str)
    }
)


def post_action(request, domain_name):
    if request.method != 'POST':
        return HttpResponse(status=405)

    if request.content_type != 'application/json':
        return HttpResponse(status=415)

    payload = json.loads(request.body)
    if not ACTION_PAYLOAD_SCHEMA.is_valid(payload):
        return HttpResponse(status=422)

    site = Site.objects.filter(domain_name=domain_name).first()

    if site:
        doc, _ = site.document_set.get_or_create(path=payload['path'])
        action = Action(document_id=doc.id, action=payload['action'])
        action.data = payload['data'] if 'data' in payload else None
        action.save()
        return HttpResponse()
    else:
        return HttpResponse(status=404)

