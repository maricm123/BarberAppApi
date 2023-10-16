from django.core.mail import send_mail


def send_mail_for_schedule(email, barber, time, date):

    subject = "Schedule Created"
    message = "Zakazivanje je proslo uspesno"
    from_email = "djujicmomo99@gmail.com"
    recipient_list = [email]
    try:

        send_mail(subject, message, from_email, recipient_list)

    except Exception as e:
        print(e)

