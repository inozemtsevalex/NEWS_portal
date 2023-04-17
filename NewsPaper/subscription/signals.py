from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from news.models import PostCategory
from news.tasks import send_notifications


# def send_notifications(preview, pk, title, subscribers):
#
#     text_content = (
#         f'Новость: {title}\n'
#         f'Ссылка на новость: http://127.0.0.1:8000/news/{pk}'
#     )
#
#     html_content = (
#         f'Новость: {preview}<br>'
#         f'<a href="http://127.0.0.1:8000/news/{pk}">'
#         f'Ссылка на новость</a>'
#     )
#     msg = EmailMultiAlternatives('Новая новость вашей подписки', text_content, None, subscribers)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribers)

