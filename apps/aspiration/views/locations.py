from rest_framework import generics, status, permissions
from utils.response import response_success, response_error

from apps.aspiration.models import Location
from apps.aspiration.serializers import LocationSerializer 


class LocationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = Location.objects.all().order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="Daftar Lokasi berhasil diambil", data=serializer.data)
    
class LocationCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser] 
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(
                message="Lokasi berhasil dibuat", 
                data=serializer.data, 
                status_code=status.HTTP_201_CREATED
            )
        return response_error(message="Gagal membuat Lokasi", errors=serializer.errors)


class LocationDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response_success(message="Detail Lokasi ditemukan", data=serializer.data)
        except Exception as e:
            return response_error(message="Lokasi tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return response_success(message="Lokasi berhasil diperbarui", data=serializer.data)
            return response_error(message="Gagal memperbarui Lokasi", errors=serializer.errors)
        except Exception as e:
            return response_error(message="Lokasi tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return response_success(message="Lokasi berhasil dihapus")
        except Exception as e:
            return response_error(message="Lokasi tidak ditemukan atau gagal dihapus", status_code=status.HTTP_404_NOT_FOUND)