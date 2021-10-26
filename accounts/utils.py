from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    message = f"""Congratulations! Вы зарегестрированы ны нашем сайте. 
              Пройдите активацию: {activation_code}"""
    send_mail('Активация аккаунта',
              message,
              'test@gmail.com',
              [email],
              )
