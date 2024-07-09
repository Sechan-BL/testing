from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

def jwt_auth_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            jwt_auth = JWTAuthentication()
            authentication_result = jwt_auth.authenticate(request)
            if authentication_result is None:
                raise AuthenticationFailed('Authentication credentials were not provided.')
            user, token = authentication_result
            request.user = user
            request.auth = token
        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view
