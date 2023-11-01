#tasks.py

from celery import shared_task
from django.core.mail import send_mail
from config import settings
from config.celery import app

# @shared_task(bind=True)
# def send_notification_mail(self, target_mail, message):
#     mail_subject = "Welcome on Board!"
#     send_mail(
#         subject = mail_subject,
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[target_mail],
#         fail_silently=False,
#         )
#     return "Done"

@shared_task(bind=True)
def send_mail_for_schedule(self, email, barber, time, date):
    print("USLO U SEND MAIL")
    subject = "Šišanje zakazano"
    message = f"Dobar dan, uspešno ste zakazali šišanje kod {barber}. Vreme sisanja: {time}, Datum sisanja: {date}"
    from_email = "djujicmomo99@gmail.com"
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(e, "SEND MAIL ERROR ")