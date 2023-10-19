"""
Contain views to make API browsable, in a web browser for instance.
"""

from api.mixins import APIRootViewMixin
# from ...permissions import CanUseTills


class ApiAPIRootView(APIRootViewMixin):
    url_namespace = "api"
    # permission_classes = (CanUseTills,)

    def get_endpoints(self):
        from ..urls import endpoints_urlpatterns
        print(endpoints_urlpatterns, "ASDASD")

        return endpoints_urlpatterns
