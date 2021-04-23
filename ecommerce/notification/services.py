from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .decorators import process_async


@process_async
def notification_send_mail(*, title: str, content: str, to=[]):
    """This function allow send email


    Parameters:
    title -- Title email
    content -- Content and body email
    to -- List users to send email
    """
    if not isinstance(to, list):
        to = list(to)
        
    message = EmailMultiAlternatives(title, content, settings.EMAIL_HOST_USER,to)
    message.attach_alternative(content, 'text/plain')
    message.send(fail_silently=True)
    