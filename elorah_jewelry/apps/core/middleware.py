import uuid
from django.shortcuts import render
from .models import SiteConfig

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = str(uuid.uuid4())
        response = self.get_response(request)
        response['X-Request-ID'] = request.id
        return response

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/management/'):
            config = SiteConfig.get()
            if config.maintenance_mode and not request.user.is_staff:
                return render(request, 'errors/503.html', status=503)
        return self.get_response(request)
