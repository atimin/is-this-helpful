import json
import logging
from schema import Schema, And, Use, Optional
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from docsite.models import Site, Action


ACTION_PAYLOAD_SCHEMA = Schema(
    {
        'path': And(str),
        'action': And(Use(str), lambda a: a in ['VIEW', 'HELPFUL', 'NOT_HELPFUL']),
        Optional('data'): And(str)
    }
)

LOGGER = logging.getLogger(__file__)


@csrf_exempt
def post_action(request, domain_name):
    if request.method == 'POST':

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
    elif request.method == 'OPTIONS':
        response = HttpResponse(status=200)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response

    return HttpResponse(status=405)

