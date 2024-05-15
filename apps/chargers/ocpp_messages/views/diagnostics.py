from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

class DiagnosticsFileUploadView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            uploaded_file = request.FILES['file']
            file_path = settings.MEDIA_ROOT.joinpath(f"{timezone.now()}{uploaded_file.name}")
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
