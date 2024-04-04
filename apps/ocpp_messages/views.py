from rest_framework.response import Response


def default_index(request):
    return Response(status=200)
