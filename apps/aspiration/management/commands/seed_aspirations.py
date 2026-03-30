import random
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files.base import ContentFile

from apps.user.models import CoreUser, CoreStudent, CoreAdmin
from apps.aspiration.models.categories import Category
from apps.aspiration.models.locations import Location
from apps.aspiration.models.aspirations import Aspiration, AspirationProgress, AspirationFile

class Command(BaseCommand):
    help = "Seed database with Users (Student & Admin profiles) and 20 varied Aspiration data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning old data...")
        
        AspirationProgress.objects.all().delete()
        AspirationFile.objects.all().delete()
        Aspiration.objects.all().delete()
        
        CoreUser.objects.filter(is_superuser=False).delete()

        self.stdout.write("Seeding Users, Students, & Admins...")

        with transaction.atomic():
            users = []
            rombels = ["PPLG XI-1", "PPLG XI-2", "PPLG XI-3", "PPLG XI-4"]
            rayons = ["Cicurug 1", "Cicurug 2", "Ciawi 1", "Ciawi 2", "Tajur 1"]
            
            for i in range(1, 6):
                email = f"siswa{i}@sekolah.id"
                user, created = CoreUser.objects.get_or_create(
                    email=email,
                    defaults={'is_staff': False}
                )
                if created:
                    user.set_password('password123')
                    user.save()
                    
                    CoreStudent.objects.create(
                        user=user,
                        nis=120000 + i, 
                        name=f"Siswa Dummy {i}",
                        rombel=random.choice(rombels),
                        rayon=random.choice(rayons)
                    )
                users.append(user)

            admins = []
            for i in range(1, 3):
                email = f"admin{i}@sekolah.id"
                admin, created = CoreUser.objects.get_or_create(
                    email=email,
                    defaults={'is_staff': True}
                )
                if created:
                    admin.set_password('admin123')
                    admin.save()
                    
                    CoreAdmin.objects.create(
                        user=admin,
                        name=f"Admin Dummy {i}"
                    )
                admins.append(admin)

            self.stdout.write(self.style.SUCCESS(f"Created {len(users)} Students and {len(admins)} Admins."))

            categories_data = ['Fasilitas', 'Lingkungan', 'Pendidikan', 'Karakter', 'Ibadah', 'Kesehatan']
            category_objs = [Category.objects.get_or_create(name=name)[0] for name in categories_data]

            locations_data = ['G. Padjajaran 1', 'G. Siliwangi', 'Lapangan Utama', 'Balai Krida', 'Perpustakaan', 'Kantin', 'Masjid', 'UKS']
            location_objs = [Location.objects.get_or_create(name=name)[0] for name in locations_data]

            aspiration_samples = [
                {"title": "Keran Air Wudhu Bocor", "desc": "Keran di area masjid sebelah kanan bocor terus menerus, air jadi terbuang sia-sia."},
                {"title": "Lampu Kelas Redup", "desc": "Beberapa lampu di ruang kelas mulai berkedip dan redup, mengganggu konsentrasi belajar."},
                {"title": "Sirkulasi Udara Lab Komputer", "desc": "Ruangan terasa sangat pengap saat praktikum karena salah satu AC tidak dingin."},
                {"title": "Update Buku Literasi", "desc": "Mohon perbanyak koleksi buku fiksi terbaru di perpustakaan untuk minat baca siswa."},
                {"title": "Kebersihan Area Kantin", "desc": "Banyak sampah plastik yang tidak terangkut di belakang meja kantin saat jam istirahat kedua."},
                {"title": "Jadwal Penggunaan Lapangan", "desc": "Mohon diperjelas jadwal pemakaian lapangan agar tidak bentrok antar ekskul."},
                {"title": "Penyediaan Sabun Cuci Tangan", "desc": "Wastafel di depan kelas sering kehabisan sabun cuci tangan."},
                {"title": "Koneksi Wifi Terputus", "desc": "Wifi sekolah sering tidak bisa diakses saat jam-jam kritis pengerjaan tugas."},
                {"title": "Meja Belajar Rusak", "desc": "Ada beberapa meja yang permukaannya sudah tidak rata dan tajam, membahayakan seragam."},
                {"title": "Penambahan Tempat Sampah", "desc": "Perlu tambahan tempat sampah di koridor lantai 2 karena jaraknya terlalu jauh."},
                {"title": "Kondisi Toilet Siswa", "desc": "Bau tidak sedap di toilet lantai 1 mohon segera ditangani oleh tim kebersihan."},
                {"title": "Program Infaq Jumat", "desc": "Saran untuk transparansi dana infaq jumat agar dipajang di mading masjid."},
                {"title": "Alat Olahraga Kurang", "desc": "Bola basket banyak yang sudah kempes, mohon pengadaan alat baru."},
                {"title": "Parkir Sepeda Berantakan", "desc": "Mohon ada petugas atau garis pembatas agar parkir sepeda lebih rapi."},
                {"title": "Suara Speaker Kelas", "desc": "Speaker pengumuman di kelas kami suaranya pecah dan tidak terdengar jelas."},
                {"title": "Request Menu Kantin Sehat", "desc": "Mohon ditambah variasi menu sayuran atau buah potong di kantin."},
                {"title": "Cermin UKS Pecah", "desc": "Ada cermin di ruang UKS yang retak, mohon segera diganti sebelum melukai orang."},
                {"title": "Kegiatan Ekstrakurikuler", "desc": "Mohon ditambah pilihan ekskul di bidang desain grafis atau coding."},
                {"title": "Keamanan Loker Siswa", "desc": "Beberapa kunci loker sudah mulai dol, mohon dicek kembali keamanannya."},
                {"title": "Tanaman Kering di Taman", "desc": "Taman di depan gedung utama terlihat kurang terawat dan banyak tanaman mati."}
            ]
            
            statuses = ['menunggu', 'proses', 'selesai', 'dibatalkan']

            self.stdout.write("Seeding 20 Aspirations with images...")

            for i in range(20):  
                user = random.choice(users)
                status = random.choice(statuses)
                sample = aspiration_samples[i]
                
                aspiration = Aspiration.objects.create(
                    user=user,
                    category=random.choice(category_objs),
                    location=random.choice(location_objs),
                    status=status,
                    title=sample["title"],
                    description=sample["desc"]
                )
                
                try:
                    response = requests.get(f"https://picsum.photos/id/{random.randint(1, 100)}/800/600", timeout=5)
                    if response.status_code == 200:
                        dummy_content = ContentFile(response.content, name=f"aspiration_{aspiration.id}.jpg")
                        AspirationFile.objects.create(aspiration=aspiration, file=dummy_content)
                except Exception:
                    AspirationFile.objects.create(aspiration=aspiration, file=ContentFile(b"dummy", name="fallback.jpg"))

                AspirationProgress.objects.create(
                    aspiration=aspiration,
                    status='menunggu',
                    description="Aspirasi berhasil diterima oleh sistem."
                )

                if status in ['proses', 'selesai', 'dibatalkan']:
                    admin_user = random.choice(admins) 
                    
                    if status in ['proses', 'selesai']:
                        AspirationProgress.objects.create(
                            aspiration=aspiration,
                            admin=admin_user,
                            status='proses',
                            description=f"Sedang ditinjau oleh petugas di {aspiration.location.name}."
                        )

                    if status == 'selesai':
                        AspirationProgress.objects.create(
                            aspiration=aspiration,
                            admin=admin_user,
                            status='selesai',
                            description="Laporan sudah selesai ditangani. Terima kasih!"
                        )
                    elif status == 'dibatalkan':
                        AspirationProgress.objects.create(
                            aspiration=aspiration,
                            admin=admin_user,
                            status='dibatalkan',
                            description="Laporan dibatalkan/ditolak karena data tidak valid."
                        )

            self.stdout.write(self.style.SUCCESS("Successfully seeded everything!"))