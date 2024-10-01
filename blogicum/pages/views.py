from django.views.generic import TemplateView
from django.shortcuts import render


class AboutTemplateView(TemplateView):
    template_name = 'pages/about.html'
    
class RulestTemplateView(TemplateView):
    template_name = 'pages/rules.html'
    

def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)

def internal_server_error500(request):
    return render(request, 'pages/500.html', status=500)

