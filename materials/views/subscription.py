from drf_yasg import openapi
from drf_yasg.openapi import TYPE_INTEGER, TYPE_STRING
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from materials.models import Subscription, Course


class SubscriptionAPIView(APIView):

    @swagger_auto_schema(operation_description="Test",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'course_id': openapi.Schema(
                                     type=TYPE_INTEGER,
                                     description="Id of the course")
                             },
                             responses={
                                 204: openapi.Response(
                                     description="OK",
                                     schema=openapi.Schema(
                                         type=openapi.TYPE_OBJECT,
                                         properties={
                                             'message': openapi.Schema(
                                                 type=TYPE_STRING,
                                                 description="Subscription delete/Subscription created")
                                         }
                                     )
                                 )
                             }
                         ))
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course_item)

        if subscription.exists():
            subscription.delete()
            message = f"Subscription delete"

        else:
            Subscription.objects.create(user=user, course=course_item).save()
            message = f"Subscription created"

        return Response({"message": message})
