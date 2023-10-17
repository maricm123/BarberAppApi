from django.core.mail import send_mail


def send_mail_for_schedule(email, barber, time, date):
    subject = "Šišanje zakazano"
    message = f"Dobar dan, uspešno ste zakazali šišanje kod {barber}. Vreme sisanja: {time}, Datum sisanja: {date}"
    from_email = "djujicmomo99@gmail.com"
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(e)

