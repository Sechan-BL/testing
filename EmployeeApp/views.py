import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
from .decorators import jwt_auth_required
from EmployeeApp.models import Employee
from serializers import TicketSerializer
from EmployeeApp.models import Ticket

# client = MongoClient('mongodb://localhost:27017/')
# dbname = client.new
# collection = dbname.new
# ticket_collection = dbname.ticket

@csrf_exempt
@jwt_auth_required
def get_employees(request):
    employees = list(collection.find())
    for employee in employees:
        employee['_id'] = str(employee['_id'])
    return JsonResponse(employees, safe=False)

@csrf_exempt
@jwt_auth_required
def create_employee(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        employee_id = data.get('id')
        if not employee_id:
            return JsonResponse(dict(error='Employee id is required'), status=400)
        if collection.find_one({'id': employee_id}):
            return JsonResponse(dict(error='Employee with this id already exists'), status=400)
        result = collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return JsonResponse(data)
    return JsonResponse(dict(error='Method not allowed'), status=405)

@csrf_exempt
@jwt_auth_required
def get_employee(request, id):
    employee = collection.find_one({'id': id})
    if employee:
        employee['_id'] = str(employee['_id'])
        return JsonResponse(employee)
    return JsonResponse(dict(error='Employee not found'), status=404)

@csrf_exempt
@jwt_auth_required
def update_employee(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        result = collection.update_one({'id': id}, {'$set': data})
        if result.matched_count:
            data['id'] = id
            employee = collection.find_one({'id': id})
            employee['_id'] = str(employee['_id'])
            return JsonResponse(employee)
        return JsonResponse(dict(error='Employee not found'), status=404)
    return JsonResponse(dict(error='Method not allowed'), status=405)

@csrf_exempt
@jwt_auth_required
def delete_employee(request, id):
    if request.method == 'DELETE':
        result = collection.delete_one({'id': id})
        if result.deleted_count:
            return JsonResponse(dict(message='Employee deleted'))
        return JsonResponse(dict(error='Employee not found'), status=404)
    return JsonResponse(dict(error='Method not allowed'), status=405)

@csrf_exempt
@jwt_auth_required
def test_api(request):
    return JsonResponse({"status":"working"})

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['with_mongo']
collection = db['tickets']

from django.db import connection
import json

# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from serializers import TicketSerializer
from pymongo import MongoClient
from django.db import connection
import string
# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['with_mongo']
collection = db['tickets']


from rest_framework import status
@api_view(['POST'])
def create_ticket(request):
    # print("type of req.data",type(request.data))
    request.data.update({"tid": "".join(random.choice(string.ascii_uppercase) for _ in range(6))})
    print(" req.data",(request.data))
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        tid = serializer.validated_data['tid']
        assigned_to_id = serializer.validated_data['assigned_to']
        assigned_by_id = serializer.validated_data['assigned_by']
        description = serializer.validated_data['description']

        # Store ticket in MongoDB
        ticket_data = {
            'tid': tid,
            'assigned_to': assigned_to_id,
            'assigned_by': assigned_by_id,
            'description': description
        }
        collection.insert_one(ticket_data)

        # Update or insert into MySQL
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM auth_user WHERE id = %s", [assigned_to_id])
                row = cursor.fetchone()
                if row:
                    username = row[4]
                    cursor.execute(
                        "INSERT INTO EmployeeApp_employee (userid, tid, username) VALUES (%s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE tid = VALUES(tid), username = VALUES(username)",
                        [assigned_to_id, tid, username]
                    )
                else:
                    return Response({"error": "Assigned_to user not found in MySQL"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Ticket created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_tickets_by_tid(request, tid):
    ticket = collection.find_one({'tid': tid})
    if ticket:
        ticket['_id'] = str(ticket['_id'])
        return JsonResponse(ticket)
    else:
        return Response({"message": "Ticket not found in MongoDB"}, status=404)


@api_view(['GET'])
def get_tickets_by_username(request, username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT userid,tid FROM EmployeeApp_employee WHERE username = %s", [username])
        tickets = cursor.fetchall()
    return Response(tickets)
