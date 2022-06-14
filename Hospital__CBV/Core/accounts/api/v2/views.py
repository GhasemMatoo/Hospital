from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import (RegisterSerializer, CustomAuthTokenSerializer,
                          CustomTokenObtainPairSerializer, ChangePasswordSerializer,
                          ProfileSerialize, ResendActivationSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from ...models import User, Profile


class ProfileApiViews(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerialize
    queryset = Profile.objects.all()

    def get_object(self):
      queryset = self.get_queryset()
      obj = get_object_or_404(queryset, user=self.request.user)
      return obj


class RegisterApiViews(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_email = serializer.validated_data['email']
            data = {
                'email': serializer.validated_data['email']
            }
            email = get_object_or_404(User,email=user_email)
            token = self.get_tokens_for_user(email)
            message = EmailMessage('email/Activation.tpl', {'token': token}, 'Admin@gmail.com',
                                   to=[user_email])
            message.send()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiViews(APIView):
    def get(self, request, *args, **kwargs):
        try:
            token = decode(kwargs['token'], settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({'details': 'Token has expired '}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'details': 'Token has invalid '}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(id=user_id)
        user_obj.is_active = True
        user_obj.save()
        return Response({'details': 'Yor user is activation '}, status=status.HTTP_202_ACCEPTED)


class ResendActivationApiViews(generics.GenericAPIView):
    serializer_class = ResendActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResendActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user)
        message = EmailMessage('email/Activation.tpl', {'token': token},
                               'Admin@gmail.com', to=[user.email])
        message.send()
        return Response({'details': 'Resend activation link fo you '}, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ChangePasswordApiViews(generics.GenericAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer