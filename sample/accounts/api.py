from django.http import HttpResponse

from rest_framework import (
    serializers, renderers, decorators, authentication, permissions)

import models


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
@decorators.authentication_classes((authentication.BasicAuthentication,))
@decorators.permission_classes((permissions.IsAuthenticated,))
def profile_list(request):
    '''
    >>> import requests
    >>> requests.post('http://wp.deb:9990/accounts/api/profile/',
                      auth=('admin','password'))
    '''
    ser = ProfileSerializer(models.Profile.objects.all(), many=True)
    # rest_framework.serializers.ListSerializer
    return JSONResponse(ser.data)
