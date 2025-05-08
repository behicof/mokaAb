#!/bin/bash
echo "راه‌اندازی سیستم امنیتی مکعب کیهانی..."
echo "بنیان‌گذار: behicof"
echo "تاریخ پایه‌گذاری: 2025-04-17 14:59:15"
echo "در حال آماده‌سازی لایه‌های امنیتی..."
python -c "
from cosmic_security import CosmicSecuritySystem
security = CosmicSecuritySystem('behicof', '2025-04-17 14:59:15')
print('سیستم امنیتی با موفقیت راه‌اندازی شد.')
"
echo "اطلاعات امنیتی در پوشه cosmic_security ذخیره شد."
echo "لطفاً فایل رمزهای پایه را در مکان امنی نگهداری کنید."