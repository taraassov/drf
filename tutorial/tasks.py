from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(user_mail, course_title):
    subject = 'Обновление материалов курса'
    message = f'Уважаемый пользователь, материалы курса "{course_title}" были обновлены. Посетите наш сайт, чтобы узнать подробности.'
    from_email = 'yourmail@mail.com'
    send_mail(subject, message, from_email, [user_mail])
