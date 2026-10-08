from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import connection
from django.core.cache import cache

class HomeView(TemplateView):
    template_name = "core/home.html"

class AboutView(TemplateView):
    template_name = "core/about.html"

class ContactView(TemplateView):
    template_name = "core/contact.html"

def health_check(request):
    db_ok = True
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = False
        
    redis_ok = True
    try:
        cache.set("health_check", "1", timeout=1)
    except Exception:
        redis_ok = False

    status = "healthy" if db_ok and redis_ok else "unhealthy"
    status_code = 200 if status == "healthy" else 503
    
    return JsonResponse({
        "status": status,
        "database": "ok" if db_ok else "down",
        "redis": "ok" if redis_ok else "down",
    }, status=status_code)

def security_txt(request):
    return render(request, "core/security.txt", content_type="text/plain")

def legal_page(request, slug):
    return render(request, f"core/{slug}.html")

def error_400(request, exception):
    return render(request, "errors/400.html", status=400)

def error_403(request, exception):
    return render(request, "errors/403.html", status=403)

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)
