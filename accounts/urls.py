from django.conf.urls import url
from django.views import generic
from .views import change_password

urlpatterns = [
    url(r'^change-password/$', change_password),
    url(r'^change-password/success/$', generic.TemplateView.as_view(template_name='accounts/success.html'), name='success'),
]
