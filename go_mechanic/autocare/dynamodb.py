import boto3
from django.conf import settings
from uuid import uuid4
from decimal import Decimal

dynamodb = boto3.resource('dynamodb',
                         region_name=settings.AWS_DYNAMODB_REGION,
                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

users_table = dynamodb.Table('Users')
vehicles_table = dynamodb.Table('Vehicles')
records_table = dynamodb.Table('MaintenanceRecords')

def create_user(username, password_hash):
    users_table.put_item(Item={'username': username, 'password_hash': password_hash})

def get_user(username):
    response = users_table.get_item(Key={'username': username})
    return response.get('Item')

def create_vehicle(user_id, vehicle_name, model, year):
    vehicle_id = str(uuid4())
    vehicles_table.put_item(Item={
        'vehicle_id': vehicle_id,
        'user_id': user_id,
        'vehicle_name': vehicle_name,
        'model': model,
        'year': year
    })
    return vehicle_id

def get_vehicles(user_id):
    response = vehicles_table.scan(FilterExpression='user_id = :uid', ExpressionAttributeValues={':uid': user_id})
    return response.get('Items', [])

def update_vehicle(vehicle_id, user_id, vehicle_name, model, year):
    vehicles_table.update_item(
        Key={'vehicle_id': vehicle_id, 'user_id': user_id},
        UpdateExpression='SET #vn = :v, #m = :mo, #y = :y',
        ExpressionAttributeNames={'#vn': 'vehicle_name', '#m': 'model', '#y': 'year'},
        ExpressionAttributeValues={':v': vehicle_name, ':mo': model, ':y': year}
    )

def delete_vehicle(vehicle_id, user_id):
    vehicles_table.delete_item(Key={'vehicle_id': vehicle_id, 'user_id': user_id})

def create_maintenance_record(vehicle_id, service_date, description, cost):
    record_id = str(uuid4())
    records_table.put_item(Item={
        'record_id': record_id,
        'vehicle_id': vehicle_id,
        'service_date': service_date,
        'description': description,
        'cost': Decimal(str(cost))
    })
    return record_id

def get_maintenance_records(vehicle_id):
    response = records_table.scan(FilterExpression='vehicle_id = :vid', ExpressionAttributeValues={':vid': vehicle_id})
    return response.get('Items', [])