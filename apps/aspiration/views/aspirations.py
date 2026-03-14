from rest_framework import generics, status, permissions
from django.db import transaction
from utils.response import response_success, response_error

from apps.aspiration.models import Aspiration, AspirationProgress
from apps.aspiration.serializers import AspirationSerializer, AspirationProgressSerializer


class AspirationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AspirationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Aspiration.objects.all().order_by('-created_at')
        return Aspiration.objects.filter(user=user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
             return response_success(message="Belum ada data Aspirasi", data=[])

        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="List semua data Aspirasi", data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, status='menunggu')
            return response_success(
                message="Aspirasi berhasil dikirim",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return response_error(message="Gagal mengirim aspirasi", errors=serializer.errors)


class AspirationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AspirationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Aspiration.objects.all()
        return Aspiration.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response_success(message="Detail aspirasi ditemukan", data=serializer.data)
        except Exception as e:
            return response_error(message="Aspirasi tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)


class AspirationUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AspirationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Aspiration.objects.all()
        return Aspiration.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) 
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return response_success(message="Aspirasi berhasil diperbarui", data=serializer.data)
            return response_error(message="Gagal memperbarui aspirasi", errors=serializer.errors)
        except Exception as e:
            return response_error(message="Aspirasi tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return response_success(message="Aspirasi berhasil dihapus")
        except Exception as e:
            return response_error(message="Aspirasi tidak ditemukan atau gagal dihapus", status_code=status.HTTP_404_NOT_FOUND)


class AspirationProgressListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AspirationProgressSerializer

    def get_queryset(self):
        return AspirationProgress.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
             return response_success(message="Belum ada data Progress Aspirasi", data=[])

        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="List semua data Progress Aspirasi", data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                progress = serializer.save(admin=self.request.user)
                
                aspiration = progress.aspiration
                aspiration.status = progress.status
                aspiration.save()
                
            return response_success(
                message="Status aspirasi berhasil diperbarui",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return response_error(message="Gagal memperbarui status", errors=serializer.errors)
    

class AspirationProgressDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AspirationProgressSerializer
    queryset = AspirationProgress.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response_success(message="Detail progres ditemukan", data=serializer.data)
        except Exception as e:
            return response_error(message="Progres tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            if serializer.is_valid():
                with transaction.atomic():
                    progress = serializer.save()
                    
                    aspiration = progress.aspiration
                    aspiration.status = progress.status
                    aspiration.save()

                return response_success(message="Progres berhasil diperbarui", data=serializer.data)
            return response_error(message="Gagal memperbarui progres", errors=serializer.errors)
        except Exception as e:
            return response_error(message="Progres tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return response_success(message="Progres berhasil dihapus")
        except Exception as e:
            return response_error(message="Progres tidak ditemukan atau gagal dihapus", status_code=status.HTTP_404_NOT_FOUND)