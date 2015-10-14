from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework import (serializers, renderers)

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


@csrf_exempt
def profile_list(request):
    ser = ProfileSerializer(models.Profile.objects.all(), many=True)
    # rest_framework.serializers.ListSerializer
    return JSONResponse(ser.data)
