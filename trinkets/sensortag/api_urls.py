from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from sensortag import views as sensortag_views

urlpatterns = [
    url(
        regex=r"^sensortags/$",
        view=sensortag_views.SensortagListReadView.as_view(),
    ),
    url(
        regex=r"^sensortags/(?P<mac_slug>\w+)/$",
        view=sensortag_views.SensortagDetailReadUpdateView.as_view()
    ),
    url(
        regex=r"^sensortags/(?P<mac_slug>\w+)/(?P<year>[0-9]{4})/$",
        view=sensortag_views.SensortagDetailReadUpdateView.as_view()
    ),
    url(
        regex=r"^sensortags/(?P<mac_slug>\w+)/(?P<year>[0-9]{4})/\
              (?P<month>[0-9]{2})/$",
        view=sensortag_views.SensortagDetailReadUpdateView.as_view()
    ),
    url(
        regex=r"^sensortags/(?P<mac_slug>\w+)/(?P<year>[0-9]{4})/\
              (?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$",
        view=sensortag_views.SensortagDetailReadUpdateView.as_view()
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
