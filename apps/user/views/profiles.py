from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from apps.user.serializers import MeSerializer
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