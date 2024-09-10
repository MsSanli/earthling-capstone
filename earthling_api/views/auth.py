# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from earthling_api.models import User

# @api_view(['POST'])
# def check_user(request):
#     '''Checks to see if User has Associated Gamer

#     Method arguments:
#       request -- The full HTTP request object
#     '''
#     uid = request.data['uid']

#     # Use the built-in authenticate method to verify
#     # authenticate returns the user object or None if no user is found
#     user = User.objects.filter(uid=uid).first()

#     # If authentication was successful, respond with their token
#     if user is not None:
#         data = {
#             'id': user.id,
#             'uid': user.uid,
#             'name': user.name
#         }
#         return Response(data)
#     else:
#         # Bad login details were provided. So we can't log the user in.
#         data = { 'valid': False }
#         return Response(data)


# @api_view(['POST'])
# def register_user(request):
#     '''Handles the creation of a new gamer for authentication

#     Method arguments:
#       request -- The full HTTP request object
#     '''

#     # Now save the user info in the levelupapi_gamer table
#     user = User.objects.create(
#         name=request.data['name'],
#         uid=request.data['uid']
#     )

#     # Return the gamer info to the client
#     data = {
#         'id': user.id,
#         'uid': user.uid,
#         'name': user.name
#     }
#     return Response(data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from earthling_api.models import User
from django.utils import timezone
from rest_framework import status

@api_view(['POST'])
def check_user(request):
    '''Checks to see if User exists and returns user data

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data.get('uid')
    
    if not uid:
        return Response({'error': 'uid is required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(uid=uid).first()

    if user is not None:
        # Update last_login
        user.last_login = timezone.now()
        user.save()

        data = {
            'id': user.id,
            'uid': user.uid,
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at,
            'last_login': user.last_login
        }
        return Response(data)
    else:
        return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    required_fields = ['name', 'email', 'uid']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    name = request.data['name']
    email = request.data['email']
    uid = request.data['uid']

    # Check if user with this uid or email already exists
    if User.objects.filter(uid=uid).exists():
        return Response({'error': 'User with this uid already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the new user
    user = User.objects.create(
        name=name,
        email=email,
        uid=uid,
        last_login=timezone.now()  # Set initial last_login
    )

    # Return the user info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at,
        'last_login': user.last_login
    }
    return Response(data, status=status.HTTP_201_CREATED)

