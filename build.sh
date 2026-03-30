#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Kumpulkan file statis (untuk CSS/JS Admin & WhiteNoise)
python manage.py collectstatic --no-input

# 3. Jalankan migrasi database ke Supabase
python manage.py migrate --no-input

# 4. Jalankan Seeder Aspiration
# Karena filenya di apps/aspiration/management/commands/seed_aspirations.py,
# Django mengenalinya sebagai command "seed_aspirations"
echo "Running Seeders..."
python manage.py seed_aspirations

# 5. Buat Super Admin secara otomatis
# Menggunakan shell script agar tidak error jika user sudah ada
echo "Creating Superuser..."
python manage.py shell << END
from apps.user.models import CoreUser
email = 'django@gmail.com'
password = 'django'

if not CoreUser.objects.filter(email=email).exists():
    CoreUser.objects.create_superuser(email=email, password=password)
    print(f"Superuser {email} created successfully.")
else:
    print(f"Superuser {email} already exists.")
END

echo "Build Process Completed!"