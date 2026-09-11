from django.db import connection
from django.http import HttpResponse, HttpResponseServerError


def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        return HttpResponseServerError("db error", content_type="text/plain")

    return HttpResponse("ok", content_type="text/plain")
