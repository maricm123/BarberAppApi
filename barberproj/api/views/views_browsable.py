from api.mixins import APIRootViewMixin


class APIRootView(APIRootViewMixin):
    url_namespace = "api"

    def get_endpoints(self):
        from ..urls import endpoints_urlpatterns

        return endpoints_urlpatterns
