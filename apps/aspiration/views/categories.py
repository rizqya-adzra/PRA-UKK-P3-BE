from rest_framework import generics, permissions
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