from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.db.utils import OperationalError


def home(request):
    return HttpResponse("Welcome to the homepage!")
class HealthCheckView(APIView):
    def get(self, request):
        try:
            # Ensure database connection
            connection.ensure_connection()
            # Minimal success response
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except OperationalError:
            # Detailed failure response
            result = {
                "accounts": "db error",
                "recruit": "db error",
                "status": "unhealthy"
            }
            return Response(result, status=status.HTTP_503_SERVICE_UNAVAILABLE)

