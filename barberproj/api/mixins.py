from django.core.mail import send_mail
from django.urls.exceptions import NoReverseMatch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from barberproj.config import settings
"""
Accessing Request Data:
You can use this mixin when you need to access data from the incoming HTTP request, such as the user making the request, request headers, query parameters, or other request-related information.
Custom Validation:
It can be useful for custom validation logic in serializers. For example, you might want to validate a field based on the current user's permissions or some other request-specific information.
Custom Field Logic:
You might need to perform custom logic for a serializer field based on request data. For instance, you may want to show or hide certain fields based on the user making the request.
"""


class ReqContextMixin:
    @property
    def _req_context(self):
        return self.context["request"]


def send_mail_for_schedule(email, barber, time, date):
    subject = "Potvrda za zakazani termin šišanja"
    message = f"Dobar dan, uspešno ste zakazali šišanje kod frizera: {barber}. \nVreme usluge: {time}, Datum usluge: {date}. \n\n Za otkazivanje termina molimo Vas pozovite +38162419722. \n\n Hvala na poverenju!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(e)


class APIRootViewMixin(APIView):
    """
    Return a dict endpoint_name: url for a rest api.
    Url needing an extra parameter (often a pk) are not displayed.
    """

    url_namespace = None

    def get_endpoints(self):
        raise NotImplementedError

    def get(self, request):
        self._check_url_namespace()
        list_endpoints = self.get_endpoints()

        dict_endpoints = dict(url_without_parameters=dict(), url_with_parameters=dict())
        for endpoint_path in list_endpoints:
            name = endpoint_path.name
            try:
                uri = request.build_absolute_uri(reverse(f"{self.url_namespace}:{name}"))
                key = "url_without_parameters"
            except NoReverseMatch:
                uri = request.build_absolute_uri(endpoint_path.pattern._route)
                key = "url_with_parameters"

            dict_endpoints[key][name] = uri

        return Response(dict_endpoints)

    def _check_url_namespace(self):
        if not self.url_namespace:
            raise AttributeError("Set url namespace")