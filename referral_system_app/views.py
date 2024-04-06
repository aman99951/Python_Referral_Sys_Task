from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from .models import User, Referral
from .serializers import UserSerializer, ReferralSerializer
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'user_id': user.id,
                'message': 'User registered successfully.'
            }
            return JsonResponse(data, status=201)
        return JsonResponse(serializer.errors, status=400)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class ReferralsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add permission_classes
    serializer_class = ReferralSerializer
    lookup_field = 'referral_code'

    def get_queryset(self):
        if self.request.user.is_authenticated:  # Check if user is authenticated
            referral_code = self.request.user.referral_code
            return Referral.objects.filter(user__referral_code=referral_code)
        else:
            return Referral.objects.none()  # Return empty queryset if user is not authenticated
