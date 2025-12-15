# MiniCRM – Customer & Deals Management API

پیاده‌سازی کامل یک CRM مینیمال با FastAPI، معماری Clean، PostgreSQL، Alembic و SQLAlchemy (async).

## اجزای اصلی
- Customers, Activities, Deals, Tasks
- معماری لایه‌ای: domain, application, infrastructure, presentation
- Scalar UI برای مستندات OpenAPI در مسیر `/docs`

## راه‌اندازی سریع
1. وابستگی‌ها را نصب کنید:
   ```bash
   pip install -r requirements.txt
   ```
2. متغیر محیطی `DATABASE_URL` را مقداردهی کنید (مثال: `postgresql+asyncpg://user:pass@localhost:5432/minicrm`).
3. مهاجرت دیتابیس:
   ```bash
   alembic upgrade head
   ```
4. اجرای برنامه:
   ```bash
   uvicorn presentation.main:app --reload
   ```

## ساختار پروژه
- `src/domain`: موجودیت‌ها و قواعد بیزنسی (بدون وابستگی فریم‌ورک)
- `src/application`: سرویس‌ها/Use Case ها که UoW را orchestration می‌کنند
- `src/infrastructure`: مدل‌های ORM، ریپوزیتوری‌ها و UnitOfWork مبتنی بر SQLAlchemy async
- `src/presentation`: FastAPI routers, dependency wiring, main app + healthcheck/Scalar
- `alembic`: تنظیمات و نسخه اولیه اسکیما

## تست‌ها
```bash
pytest
```

## نقاط کلیدی بیزنسی
- Customer: وضعیت‌ها (NEW/ACTIVE/INACTIVE) و ممنوعیت آرشیو در صورت وجود دیل فعال
- Deal: انتقال Stage فقط در صورت غیر بسته بودن (WON/LOST) و ثبت Activity اتوماتیک هنگام برد/باخت
- Task: تکمیل فقط از وضعیت PENDING و رد کردن سررسید خیلی قدیمی

