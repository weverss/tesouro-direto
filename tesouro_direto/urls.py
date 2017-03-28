from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from tesouro_direto import views

router = DefaultRouter()
router.register(r'titulo_tesouro', views.OperacaoTituloViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
