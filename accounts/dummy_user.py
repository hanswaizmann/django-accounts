from django.contrib.auth import get_user_model

def create_dummy_user():
    email = 'john@doe.com'
    first_name = 'John'
    last_name = 'Doe'
    password = 'secret123'
    UserModel = get_user_model()
    user = UserModel.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
    return user

dummy_user = {
    'email': 'john@doe.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'password': 'secret123',
}
