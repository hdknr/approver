from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from rest_framework import (
    serializers, renderers, decorators, authentication, permissions)
import models

from approver.rests.authentication import BearerTokenAuthentication
from approver.models import Token


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = renderers.JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('id', 'birth_year', 'birth_month', 'birth_day', )

    def response(self):
        return JSONResponse(self.data)


@decorators.api_view(['GET', 'POST'])
@decorators.authentication_classes(
    (BearerTokenAuthentication, authentication.BasicAuthentication,))
@decorators.permission_classes((permissions.IsAuthenticated,))
@permission_required('accounts.change_profile')
def profile_list(request):
    '''
    BasicAuthentication

    >>> import requests
    >>> requests.post('http://wp.deb:9990/accounts/api/profile/',
                      auth=('admin','password'))

    BearerTokenAuthentication

    >>>  requests.get('http://wp.deb:9990/accounts/api/profile/',
                      headers={'Authorization': 'Bearer my_token_string'})
    '''
    assert request.user and isinstance(request.auth, Token)

    ser = ProfileSerializer(models.Profile.objects.all(), many=True)
    # rest_framework.serializers.ListSerializer
    return JSONResponse(ser.data)
