from django.conf.urls import url
import api


urlpatterns = [
    url(r'api/profile/', api.profile_list,
        name='accounts_api_profile_list'),
]
