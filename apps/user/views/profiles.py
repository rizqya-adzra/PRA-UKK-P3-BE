from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count

from apps.user.serializers import MeSerializer, ChangePasswordSerializer, UserAspirationRankingSerializer
from apps.user.models import CoreUser as User
from utils.response import response_success, response_error 


class MyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = MeSerializer 
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_success(
            message="Berhasil mengambil data profil",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return response_success(
                message="Profil berhasil diperbarui",
                data=serializer.data
            )
        return response_error(
            message="Gagal memperbarui profil, mohon periksa input Anda.",
            errors=serializer.errors
        )
        
        
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = self.get_object()
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            try:
                request.user.auth_token.delete()
            except (AttributeError, Exception):
                pass

            return response_success(
                message="Password berhasil diperbarui. Silakan login kembali."
            )
        
        return response_error(message="Gagal ganti password", errors=serializer.errors)
    
    
class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    
    serializer_class = MeSerializer 
    
    queryset = User.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_pages = self.paginator.page.paginator.num_pages
            current_page = self.paginator.page.number
            
            return response_success(
                message="Berhasil mengambil data semua pengguna",
                data=serializer.data,
                current_page=current_page,
                total_pages=total_pages
            )

        serializer = self.get_serializer(queryset, many=True)
        return response_success(
            message="Berhasil mengambil data semua pengguna",
            data=serializer.data
        )
        
class UserAspirationRankingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = UserAspirationRankingSerializer 

    def get_queryset(self):
        return User.objects.annotate(
            aspiration_count=Count('asp_aspirations')
        ).filter(
            aspiration_count__gt=0, 
            is_staff=False 
        ).order_by('-aspiration_count')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_pages = self.paginator.page.paginator.num_pages
            current_page = self.paginator.page.number
            
            return response_success(
                message="Berhasil mengambil peringkat aspirasi pengguna",
                data=serializer.data,
                current_page=current_page,
                total_pages=total_pages
            )

        serializer = self.get_serializer(queryset, many=True)
        return response_success(
            message="Berhasil mengambil peringkat aspirasi pengguna",
            data=serializer.data
        )