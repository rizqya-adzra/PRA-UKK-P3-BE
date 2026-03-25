from rest_framework.views import APIView
from rest_framework import generics, status, permissions, filters
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from apps.aspiration.models.aspirations import AspirationFile
from utils.response import response_success, response_error
from rest_framework.pagination import PageNumberPagination

from apps.aspiration.models import Aspiration, AspirationProgress
from apps.aspiration.serializers import AspirationSerializer, AspirationProgressSerializer
from apps.aspiration.filters import AspirationFilter

import openpyxl
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template


def generate_excel_response(queryset, filename="Data_Aspirasi.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Aspirasi"

    headers = ['Report ID', 'Judul', 'Kategori', 'Status', 'Tanggal Dibuat', 'Lokasi', 'Pengirim']
    ws.append(headers)

    for obj in queryset:
        pengirim = obj.user.student_profile.name if hasattr(obj.user, 'student_profile') else obj.user.username
        kategori = obj.category.name if getattr(obj, 'category', None) else "-"
        status_display = obj.get_status_display() if hasattr(obj, 'get_status_display') else obj.status
        tanggal = obj.created_at.strftime('%Y-%m-%d %H:%M') if obj.created_at else "-"

        ws.append([
            obj.report_id,
            obj.title,
            kategori,
            status_display,
            tanggal,
            obj.location,
            pengirim
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    
    return response

def generate_detail_pdf_response(instance, request, filename="Detail_Aspirasi.pdf"):
    template_path = 'pdf/aspiration_detail.html'
    
    context = {
        'aspiration': instance,
        'user': request.user,
        'progress_updates': instance.progress_updates.all().order_by('-created_at') if hasattr(instance, 'progress_updates') else []
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Terjadi kesalahan saat generate PDF', status=500)
        
    return response


class AspirationPagination(PageNumberPagination):
    page_size = 10              
    page_query_param = 'page'   
    page_size_query_param = 'page_size' 
    max_page_size = 50


class AspirationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AspirationSerializer
    
    pagination_class = AspirationPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AspirationFilter
    
    search_fields = [
        'user__student_profile__name',
        'user__student_profile__nis',
        'user__student_profile__rombel',
        'user__student_profile__rayon',
        'report_id',     
        'title',
        'location'          
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = Aspiration.objects.select_related('user', 'user__student_profile')
        if user.is_staff:
            return queryset.all().order_by('-created_at')
        return queryset.filter(user=user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if request.query_params.get('export') == 'excel':
            page = self.paginate_queryset(queryset)
            data_to_export = page if page is not None else queryset
            
            return generate_excel_response(data_to_export, "List_Semua_Aspirasi.xlsx")
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            
            total_pages = self.paginator.page.paginator.num_pages
            current_page = self.paginator.page.number
            
            return response_success(
                message="List semua data Aspirasi", 
                data=serializer.data,
                current_page=current_page,
                total_pages=total_pages
            )

        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="List semua data Aspirasi", data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            aspiration = serializer.save(user=self.request.user, status='menunggu')
            files = request.FILES.getlist('attachments')
            if files:
                for f in files:
                    AspirationFile.objects.create(
                        aspiration=aspiration, 
                        file=f
                    )
            response_serializer = self.get_serializer(aspiration)
            
            return response_success(
                message="Aspirasi berhasil dikirim",
                data=response_serializer.data,
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
            
            if request.query_params.get('export') == 'pdf':
                filename = f"Bukti_Aspirasi_{instance.report_id}.pdf"
                return generate_detail_pdf_response(instance, request, filename)

            serializer = self.get_serializer(instance)
            return response_success(message="Detail aspirasi ditemukan", data=serializer.data)
            
        except Exception as e:
            print(f"Error di AspirationDetailView: {e}") 
            return response_error(message="Aspirasi tidak ditemukan atau terjadi kesalahan", status_code=status.HTTP_404_NOT_FOUND)


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
                
                files = request.FILES.getlist('attachments')
                if files:
                    for f in files:
                        AspirationFile.objects.create(
                            aspiration=aspiration,
                            progress=progress,
                            file=f
                        )
                
            return response_success(
                message="Status aspirasi berhasil diperbarui",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return response_error(message="Gagal memperbarui status", errors=serializer.errors)
    

class AspirationProgressDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AspirationProgressSerializer
    queryset = AspirationProgress.objects.all().order_by('-created_at')

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
        

class AspirationStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff:
            base_query = Aspiration.objects.all()
        else:
            base_query = Aspiration.objects.filter(user=user)

        filterset = AspirationFilter(request.GET, queryset=base_query)
        if filterset.is_valid():
            base_query = filterset.qs

        stats = {
            "total": base_query.count(),
            "selesai": base_query.filter(status='selesai').count(),
            "proses": base_query.filter(status='proses').count(),
            "menunggu": base_query.filter(status='menunggu').count(),
        }

        return response_success(
            data=stats,
            message="Berhasil mengambil statistik"
        )
        
class AspirationCategoryStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        base_query = Aspiration.objects.all()        

        filterset = AspirationFilter(request.GET, queryset=base_query)
        if filterset.is_valid():
            base_query = filterset.qs
            
        stats = {
            "fasilitas": base_query.filter(category="bea0bfff-b4a7-4dae-a8a3-78ea6756e703").count(),
            "lingkungan": base_query.filter(category="d4b3f29e-0995-4709-9825-0ca48a87dbb0").count(),
            "pendidikan": base_query.filter(category="4a7b9e07-9a43-4426-9eef-74987aa467a5").count(),
            "karakter": base_query.filter(category="3541c7b7-ec66-402f-bea1-6d2dc63752a7").count(),
            "ibadah": base_query.filter(category="60180a56-2df6-4b2e-bb32-43844d7afb86").count(),
        }
        
        return response_success(
            data=stats,
            message="Berhasil mengambil statistik kategori"
        )
        
class AspirationHistoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AspirationSerializer
    
    pagination_class = AspirationPagination
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AspirationFilter
    
    search_fields = [
        'user__student_profile__name',
        'user__student_profile__nis',
        'user__student_profile__rombel',
        'user__student_profile__rayon',
        'report_id',     
        'title',
        'location'          
    ]

    def get_queryset(self):
        user = self.request.user
        target_statuses = ['selesai', 'dibatalkan']
        queryset = Aspiration.objects.select_related('user', 'user__student_profile')
        
        if user.is_staff:
            return Aspiration.objects.filter(status__in=target_statuses).order_by('-created_at')
            
        return queryset.objects.filter(user=user, status__in=target_statuses).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if request.query_params.get('export') == 'excel':
            page = self.paginate_queryset(queryset)
            data_to_export = page if page is not None else queryset
            return generate_excel_response(data_to_export, "Riwayat_Aspirasi.xlsx")
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            
            total_pages = self.paginator.page.paginator.num_pages
            current_page = self.paginator.page.number
            
            return response_success(
                message="List riwayat Aspirasi", 
                data=serializer.data,
                current_page=current_page,
                total_pages=total_pages
            )

        serializer = self.get_serializer(queryset, many=True)
        return response_success(
            message="List riwayat Aspirasi (Selesai/Dibatalkan)", 
            data=serializer.data
        )