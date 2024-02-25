from django.urls import path
from rest_framework import routers


from materials.apps import MaterialsConfig
from materials.views.course import CourseViewSet
from materials.views.lessons import LessonsListAPIView, LessonCreateAPIView, LessonDetailAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView
from materials.views.subscription import SubscriptionAPIView

app_name = MaterialsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


urlpatterns = [
    path('', LessonsListAPIView.as_view(), name='lessons_list'),
    path('create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('detail/<int:pk>/', LessonDetailAPIView.as_view(), name='lessons_detail'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lessons_delete'),

    #  subscription
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription')
] + router.urls
