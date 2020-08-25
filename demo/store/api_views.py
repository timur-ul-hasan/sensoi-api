from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer
from .models import User

class UserCreateList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('name', 'email')


