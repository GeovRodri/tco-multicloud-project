from django.conf.urls import url
from website.views import Pesquisa

urlpatterns = [
    url('', Pesquisa.as_view())
]
