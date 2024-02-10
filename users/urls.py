from rest_framework import routers

from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')


urlpatterns = [

] + router.urls
