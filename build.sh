#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Kumpulkan file statis (untuk CSS/JS Admin)
python manage.py collectstatic --no-input

# Jalankan migrasi database ke Supabase secara otomatis
python manage.py migrate