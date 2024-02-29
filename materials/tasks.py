from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription, Course


@shared_task
def send_email_to_subscribers(course: int) -> None:
    course_name = Course.objects.get(pk=course)
    subscribers_email = [subs.user.email for subs in Subscription.objects.filter(course_id=course)]
    send_mail(
        subject=f'Обновление курса -  {course_name}',
        message=f'Курс - {course_name} на который Вы подписаны был обновлен',
        from_email=EMAIL_HOST_USER,
        recipient_list= subscribers_email,
        fail_silently=False,
    )
