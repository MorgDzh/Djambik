from django.core.mail import send_mail
from djumbik._celery import app

@app.task
def notify_user_task(email):
    send_mail(
        'Вы создали новый запрос!',
        'Спасибо за использование нашего сайта.',
        'test@gmail.com',
        [email, ]
    )
    return "sucess"




