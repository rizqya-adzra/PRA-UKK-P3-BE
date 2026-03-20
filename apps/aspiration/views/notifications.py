from rest_framework import generics, status, permissions
from utils.response import response_success, response_error
from rest_framework.authentication import TokenAuthentication

from apps.aspiration.models import Notification
from apps.aspiration.serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="Notifikasi berhasil diambil", data=serializer.data)


class NotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return response_success(message="Notifikasi ditandai telah dibaca")
        except Notification.DoesNotExist:
            return response_error(message="Notifikasi tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)
        
        
class NotificationReadAllView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Notification.objects.all() 

    def post(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        
        updated_count = notifications.count()
        
        if updated_count == 0:
            return response_success(message="Tidak ada notifikasi baru untuk ditandai")

        notifications.update(is_read=True)

        return response_success(message=f"{updated_count} notifikasi ditandai telah dibaca")
        
        
class NotificationDetailDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response_success(message="Detail notifikasi ditemukan", data=serializer.data)
        except Exception as e:
            return response_error(message="Notifikasi tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return response_success(message="Notifikasi berhasil dihapus")
        except Exception as e:
            return response_error(message="Notifikasi tidak ditemukan atau gagal dihapus", status_code=status.HTTP_404_NOT_FOUND)