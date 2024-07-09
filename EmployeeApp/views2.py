from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .decorators import jwt_auth_required


@csrf_exempt
@jwt_auth_required
def test_api(request):
    return JsonResponse({"status":"working test_api2"})


