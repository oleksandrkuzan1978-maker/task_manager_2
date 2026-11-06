"""API списка пользователей с фильтрацией по проекту и регистрации пользователей."""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.users.models import User
from apps.users.serializers.users import UserListSerializer, RegisterUserSerializer

class UserListGenericView(ListAPIView):
    """Получение пользователей с необязательным фильтром по названию проекта."""
    serializer_class = UserListSerializer

    def get_queryset(self):
        """Вернуть всех пользователей либо пользователей проекта из параметра project_name."""
        project_name = self.request.query_params.get('project_name')
        if project_name:
            return User.objects.filter(project__title=project_name)
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        """Вернуть список пользователей с кодом 200 либо ответ 204 при пустой выборке."""
        projects = self.get_queryset()

        if not projects.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserGenericView(CreateAPIView):
    """Регистрация пользователя через проверку и сохранение данных сериализатором."""
    serializer_class = RegisterUserSerializer

    def create(self, request: Request, *args, **kwargs) ->Response:
        """Проверить данные, создать пользователя и вернуть его данные с кодом 201."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

