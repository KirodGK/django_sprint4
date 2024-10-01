from django.urls import path
from . import views

app_name = 'pages'

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server_error500'

urlpatterns = [
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('rules/', views.RulestTemplateView.as_view(), name='rules')
]
