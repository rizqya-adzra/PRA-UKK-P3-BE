from rest_framework import generics, status, permissions
from utils.response import response_success, response_error

from apps.aspiration.models import Category
from apps.aspiration.serializers import CategorySerializer 


class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="Daftar kategori berhasil diambil", data=serializer.data)
    
class CategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser] 
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(
                message="Kategori berhasil dibuat", 
                data=serializer.data, 
                status_code=status.HTTP_201_CREATED
            )
        return response_error(message="Gagal membuat kategori", errors=serializer.errors)


class CategoryDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response_success(message="Detail kategori ditemukan", data=serializer.data)
        except Exception as e:
            return response_error(message="Kategori tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return response_success(message="Kategori berhasil diperbarui", data=serializer.data)
            return response_error(message="Gagal memperbarui kategori", errors=serializer.errors)
        except Exception as e:
            return response_error(message="Kategori tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return response_success(message="Kategori berhasil dihapus")
        except Exception as e:
            return response_error(message="Kategori tidak ditemukan atau gagal dihapus", status_code=status.HTTP_404_NOT_FOUND)