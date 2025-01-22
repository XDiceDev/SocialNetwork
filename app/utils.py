from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.mail import send_mail

def generate_email_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-confirmation-salt')

def confirm_email_token(token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)  # 1 час
        return email
    except:
        return None



def send_confirmation_email(user):
    token = generate_email_token(user.email)
    confirmation_url = f"http://127.0.0.1:8000/confirm-email/{token}/"

    subject = 'Подтверждение почты'
    message = f'Здравствуйте {user.username},\nПодтвердите адрес своей электронной почты по ссылке ниже:\n{confirmation_url}'
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])