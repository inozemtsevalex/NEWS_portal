from celery import shared_task
from django.core.mail import EmailMultiAlternatives
import datetime
from django.template.loader import render_to_string
from news.models import Post, Category


@shared_task
def send_notifications(preview, pk, title, subscribers):
    text_content = (
        f'Новость: {title}\n'
        f'Ссылка на новость: http://127.0.0.1:8000/news/{pk}'
    )

    html_content = (
        f'Новость: {preview}<br>'
        f'<a href="http://127.0.0.1:8000/news/{pk}">'
        f'Ссылка на новость</a>'
    )
    msg = EmailMultiAlternatives('Новая новость вашей подписки', text_content, None, subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_news_subscription():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(createDate__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': 'http://127.0.0.1:8000',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Подборка за неделю',
        body='',
        from_email=None,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
