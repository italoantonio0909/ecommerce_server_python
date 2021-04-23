from .selectors import (
    user_by_id
)
from ecommerce.notification.services import notification_send_mail
from .models import BaseUser


def user_create_notify(
    *,
    user_id: int
    )-> BaseUser:

    user = user_by_id(user_id=user_id)

    title = 'Creación de cuenta'
    content = f'{user.first_name} {user.last_name} se creo su cuenta. '\
              'Estaremos comunicando sobre ofertas y promociones.'

    user_email = [user.email]
    notification_send_mail(title=title, content=content, to=user_email)
    
    return user



def user_password_change_notify(
    *,
    user_id: int
    )-> BaseUser:

    user = user_by_id(user_id=user_id)

    title = 'Password updated.'
    content = f'{user.first_name} {user.last_name} your password has been updated.'


    user_email = [user.email]
    notification_send_mail(title=title, content=content, to=user_email)
    
    return user



def user_update_profile_notify(
    *,
    user_id: int
    )-> BaseUser:

    user = user_by_id(user_id=user_id)

    title = 'Profile updated'
    content = f'{user.first_name} {user.last_name} your profile has been updated.'

    user_email = [user.email]
    notification_send_mail(title=title, content=content, to=user_email)
    
    return user




def user_password_reset_notify(
    *,
    user_id: int,
    token:str
    ) -> BaseUser:
    
    user = user_by_id(user_id=user_id)
    
    title = 'Reset password'
    content = f'Hello {user.first_name} {user.last_name}, '\
              f'\nCopy this code to reset your password \n {token}'

    user_email = [user.email]
    notification_send_mail(title=title, content=content, to=user_email)

    return user



def user_password_reset_check_notify(
    *,
    user_id: int
    ) -> BaseUser:
    
    user = user_by_id(user_id=user_id)
    
    title = 'Reset password success'
    content = f'Hello {user.first_name} {user.last_name} your password '\
              'has been reseted.'

    user_email = [user.email]
    notification_send_mail(title=title, content=content, to=user_email)

    return user
    