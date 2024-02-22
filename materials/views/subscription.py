from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Subscription, Course


class SubscriptionAPIView(APIView):
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
